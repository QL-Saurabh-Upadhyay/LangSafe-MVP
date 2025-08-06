#!/usr/bin/env python3
"""
LLM Firewall API-Only Implementation
Complete implementation with all scanners and optimizations
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict

import torch
import time

from ql_tracker import track

# PyTorch optimizations
torch.set_float32_matmul_precision('high')
import torch._inductor.config
torch._inductor.config.fx_graph_cache = True

# LLM Guard imports
from llm_guard.vault import Vault
from llm_guard.input_scanners import (
    Anonymize, BanCode, Code, BanTopics, Gibberish,
    InvisibleText, Language, PromptInjection, Regex,
    Secrets, Sentiment, TokenLimit, Toxicity
)
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from llm_guard.input_scanners.gibberish import MatchType as GibberishMatchType
from llm_guard.input_scanners.language import MatchType as LanguageMatchType
from llm_guard.input_scanners.prompt_injection import MatchType as PIMatchType
from llm_guard.input_scanners.regex import MatchType as RegexMatchType
from llm_guard.input_scanners.toxicity import MatchType as ToxicityMatchType

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ScannerConfig:
    """Configuration for each scanner"""
    name: str
    enabled: bool
    config: Dict[str, Any]
    description: str

class LLMFirewall:
    """Main LLM Firewall class with all scanners"""

    def __init__(self):
        self.vault = Vault()
        self.scanners = {}
        self.scanner_configs = self._initialize_scanner_configs()
        self._setup_default_scanners()

    def _initialize_scanner_configs(self) -> Dict[str, ScannerConfig]:
        """Initialize all scanner configurations"""
        return {
            'anonymize': ScannerConfig(
                name='Anonymize',
                enabled=True,
                config={
                    'preamble': 'Insert before prompt',
                    'allowed_names': ['John Doe'],
                    'hidden_names': ['Test LLC'],
                    'recognizer_conf': 'BERT_LARGE_NER_CONF',
                    'language': 'en',
                    'threshold': 0.0,
                    'use_faker': False
                },
                description='Detects and redacts PII (Personal Identifiable Information)'
            ),
            'ban_code': ScannerConfig(
                name='Ban Code',
                enabled=True,
                config={
                    'threshold': 0.5,
                    'use_onnx': True
                },
                description='Detects and blocks code snippets in prompts'
            ),
            'code': ScannerConfig(
                name='Code Validator',
                enabled=False,
                config={
                    'languages': ['Python', 'JavaScript', 'Java'],
                    'is_blocked': True,
                    'use_onnx': True
                },
                description='Validates specific programming languages in code'
            ),
            'ban_topics': ScannerConfig(
                name='Ban Topics',
                enabled=True,
                config={
                    'topics': ['violence', 'hate speech', 'illegal activities'],
                    'threshold': 0.5,
                    'use_onnx': True
                },
                description='Blocks specific topics using zero-shot classification'
            ),
            'gibberish': ScannerConfig(
                name='Gibberish',
                enabled=True,
                config={
                    'match_type': 'FULL',
                    'threshold': 0.7,
                    'use_onnx': True
                },
                description='Detects nonsensical or meaningless text'
            ),
            'invisible_text': ScannerConfig(
                name='Invisible Text',
                enabled=True,
                config={},
                description='Removes invisible Unicode characters and steganography'
            ),
            'language': ScannerConfig(
                name='Language',
                enabled=True,
                config={
                    'valid_languages': ['en'],
                    'match_type': 'FULL',
                    'threshold': 0.5,
                    'use_onnx': True
                },
                description='Validates prompt language authenticity'
            ),
            'prompt_injection': ScannerConfig(
                name='Prompt Injection',
                enabled=True,
                config={
                    'threshold': 0.5,
                    'match_type': 'FULL',
                    'use_onnx': True
                },
                description='Detects prompt injection attacks'
            ),
            'regex': ScannerConfig(
                name='Regex',
                enabled=True,
                config={
                    'patterns': [r'Bearer [A-Za-z0-9\-\._~\+/]+'],
                    'is_blocked': True,
                    'match_type': 'SEARCH',
                    'redact': True
                },
                description='Custom regex pattern matching and redaction'
            ),
            'secrets': ScannerConfig(
                name='Secrets',
                enabled=True,
                config={
                    'plugins': [
                        'OpenAIDetector',
                        'AWSKeyDetector',
                        'GitHubTokenDetector',
                        'SlackDetector',
                        'GitLabTokenDetector',
                        'StripeDetector',
                        'TwilioKeyDetector',
                        'MailchimpDetector',
                        'Base64HighEntropyString',
                        'HexHighEntropyString',
                    ],
                    'base64_limit': 4.5,
                    'hex_limit': 3.0,
                },
                description='Detects API keys, tokens, and other secrets from popular APIs'
            ),
            'sentiment': ScannerConfig(
                name='Sentiment',
                enabled=True,
                config={
                    'threshold': -0.5
                },
                description='Analyzes sentiment and blocks negative content'
            ),
            'token_limit': ScannerConfig(
                name='Token Limit',
                enabled=True,
                config={
                    'limit': 4096,
                    'encoding_name': 'cl100k_base'
                },
                description='Limits token count to prevent DoS attacks'
            ),
            'toxicity': ScannerConfig(
                name='Toxicity',
                enabled=True,
                config={
                    'threshold': 0.5,
                    'match_type': 'SENTENCE',
                    'use_onnx': True
                },
                description='Detects toxic and harmful content'
            )
        }

    def _setup_default_scanners(self):
        """Setup default enabled scanners with optimizations"""
        for scanner_name, config in self.scanner_configs.items():
            if config.enabled:
                self._create_scanner(scanner_name, config.config)

    def _create_scanner(self, scanner_name: str, config: Dict[str, Any]):
        """Create a scanner instance with given configuration"""
        try:
            if scanner_name == 'anonymize':
                recognizer_conf = BERT_LARGE_NER_CONF if config.get('recognizer_conf') == 'BERT_LARGE_NER_CONF' else None
                self.scanners[scanner_name] = Anonymize(
                    vault=self.vault,
                    preamble=config.get('preamble', ''),
                    allowed_names=config.get('allowed_names', []),
                    hidden_names=config.get('hidden_names', []),
                    recognizer_conf=recognizer_conf,
                    language=config.get('language', 'en'),
                    threshold=config.get('threshold', 0.0),
                    use_faker=config.get('use_faker', False)
                )

            elif scanner_name == 'ban_code':
                self.scanners[scanner_name] = BanCode(
                    threshold=config.get('threshold', 0.5),
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'code':
                self.scanners[scanner_name] = Code(
                    languages=config.get('languages', ['Python']),
                    is_blocked=config.get('is_blocked', True),
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'ban_topics':
                self.scanners[scanner_name] = BanTopics(
                    topics=config.get('topics', ['violence']),
                    threshold=config.get('threshold', 0.5),
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'gibberish':
                match_type = getattr(GibberishMatchType, config.get('match_type', 'FULL'))
                self.scanners[scanner_name] = Gibberish(
                    match_type=match_type,
                    threshold=config.get('threshold', 0.7),
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'invisible_text':
                self.scanners[scanner_name] = InvisibleText()

            elif scanner_name == 'language':
                match_type = getattr(LanguageMatchType, config.get('match_type', 'FULL'))
                self.scanners[scanner_name] = Language(
                    valid_languages=config.get('valid_languages', ['en']),
                    match_type=match_type,
                    threshold=config.get('threshold', 0.5),
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'prompt_injection':
                match_type = getattr(PIMatchType, config.get('match_type', 'FULL'))
                self.scanners[scanner_name] = PromptInjection(
                    threshold=config.get('threshold', 0.5),
                    match_type=match_type,
                    use_onnx=config.get('use_onnx', True)
                )

            elif scanner_name == 'regex':
                match_type = getattr(RegexMatchType, config.get('match_type', 'SEARCH'))
                self.scanners[scanner_name] = Regex(
                    patterns=config.get('patterns', []),
                    is_blocked=config.get('is_blocked', True),
                    match_type=match_type,
                    redact=config.get('redact', True)
                )

            elif scanner_name == 'secrets':
                from llm_guard.input_scanners.secrets import Secrets as SecretsScanner
                redact_mode = getattr(SecretsScanner, config.get('redact_mode', 'REDACT_PARTIAL'))
                self.scanners[scanner_name] = SecretsScanner(redact_mode=redact_mode)

            elif scanner_name == 'sentiment':
                self.scanners[scanner_name] = Sentiment(
                    threshold=config.get('threshold', 0)
                )

            elif scanner_name == 'token_limit':
                self.scanners[scanner_name] = TokenLimit(
                    limit=config.get('limit', 4096),
                    encoding_name=config.get('encoding_name', 'cl100k_base')
                )

            elif scanner_name == 'toxicity':
                match_type = getattr(ToxicityMatchType, config.get('match_type', 'SENTENCE'))
                self.scanners[scanner_name] = Toxicity(
                    threshold=config.get('threshold', 0.5),
                    match_type=match_type,
                    use_onnx=config.get('use_onnx', True)
                )

            logger.info(f"Successfully created {scanner_name} scanner")

        except Exception as e:
            logger.error(f"Failed to create {scanner_name} scanner: {str(e)}")
    @track
    def scan_prompt(self, prompt: str) -> Tuple[str, bool, Dict[str, Any]]:
        """Scan prompt through all enabled scanners"""
        results = {}
        sanitized_prompt = prompt
        overall_valid = True
        total_risk_score = 0.0

        start_time = time.time()

        for scanner_name, scanner in self.scanners.items():
            try:
                scanner_start = time.time()
                if scanner_name == 'secrets':
                    sanitized_prompt, is_valid, risk_score = self._process_secrets(scanner, prompt)
                else:
                    sanitized_prompt, is_valid, risk_score = scanner.scan(sanitized_prompt)

                scanner_time = time.time() - scanner_start
                results[scanner_name] = {
                    'is_valid': is_valid,
                    'risk_score': risk_score,
                    'processing_time': scanner_time
                }

                if not is_valid:
                    overall_valid = False

                total_risk_score += risk_score

            except Exception as e:
                logger.error(f"Error in {scanner_name} scanner: {str(e)}")
                results[scanner_name] = {
                    'is_valid': False,
                    'risk_score': 1.0,
                    'error': str(e),
                    'processing_time': 0
                }
                overall_valid = False

        total_time = time.time() - start_time

        return sanitized_prompt, overall_valid, {
            'scanner_results': results,
            'total_risk_score': total_risk_score,
            'total_processing_time': total_time,
            'active_scanners': len(self.scanners)
        }

    def update_scanner_config(self, scanner_name: str, enabled: bool, config: Dict[str, Any] = None):
        """Update scanner configuration"""
        if scanner_name in self.scanner_configs:
            self.scanner_configs[scanner_name].enabled = enabled
            if config:
                self.scanner_configs[scanner_name].config.update(config)

            if enabled and scanner_name not in self.scanners:
                self._create_scanner(scanner_name, self.scanner_configs[scanner_name].config)
            elif not enabled and scanner_name in self.scanners:
                del self.scanners[scanner_name]

    def get_scanner_configs(self) -> Dict[str, Dict]:
        """Get all scanner configurations"""
        return {name: asdict(config) for name, config in self.scanner_configs.items()}

    @track
    def _process_secrets(self, scanner, prompt: str) -> Tuple[str, bool, float]:
        """Process secrets scanning"""
        try:
            sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)
            return sanitized_prompt, is_valid, risk_score
        except Exception as e:
            logger.error(f"Error in secrets scanner: {str(e)}")
            return prompt, False, 1.0

# Flask API

firewall = LLMFirewall()

# # API Error Handler
# @app.errorhandler(400)
# def bad_request(error):
#     return jsonify({'error': 'Bad request', 'message': str(error)}), 400
#
# @app.errorhandler(404)
# def not_found(error):
#     return jsonify({'error': 'Not found'}), 404
#
# @app.errorhandler(500)
# def internal_error(error):
#     return jsonify({'error': 'Internal server error'}), 500
#
# # API Routes
# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'timestamp': time.time(),
#         'active_scanners': len(firewall.scanners)
#     })
#
# @app.route('/api/scanners', methods=['GET'])
# def get_scanners():
#     """Get all scanner configurations"""
#     return jsonify({
#         'scanners': firewall.get_scanner_configs(),
#         'active_count': len(firewall.scanners)
#     })
#
# @app.route('/api/scanners/<scanner_name>', methods=['GET'])
# def get_scanner(scanner_name):
#     """Get specific scanner configuration"""
#     configs = firewall.get_scanner_configs()
#     if scanner_name not in configs:
#         return jsonify({'error': 'Scanner not found'}), 404
#
#     return jsonify({
#         'scanner': scanner_name,
#         'config': configs[scanner_name]
#     })
#
# @app.route('/api/scanners/<scanner_name>', methods=['PUT'])
# def update_scanner(scanner_name):
#     """Update scanner configuration"""
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#
#     configs = firewall.get_scanner_configs()
#     if scanner_name not in configs:
#         return jsonify({'error': 'Scanner not found'}), 404
#
#     enabled = data.get('enabled', configs[scanner_name]['enabled'])
#     config = data.get('config', {})
#
#     try:
#         firewall.update_scanner_config(scanner_name, enabled, config)
#         return jsonify({
#             'status': 'success',
#             'scanner': scanner_name,
#             'enabled': enabled,
#             'message': f'Scanner {scanner_name} updated successfully'
#         })
#     except Exception as e:
#         return jsonify({'error': f'Failed to update scanner: {str(e)}'}), 500
#
# @app.route('/api/scan', methods=['POST'])
# def scan_prompt():
#     """Scan a prompt through the firewall"""
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#
#     prompt = data.get('prompt', '')
#     if not prompt:
#         return jsonify({'error': 'No prompt provided'}), 400
#
#     try:
#         sanitized_prompt, is_valid, results = firewall.scan_prompt(prompt)
#
#         return jsonify({
#             'original_prompt': prompt,
#             'sanitized_prompt': sanitized_prompt,
#             'is_valid': is_valid,
#             'risk_score': results['total_risk_score'],
#             'processing_time_ms': results['total_processing_time'] * 1000,
#             'active_scanners': results['active_scanners'],
#             'scanner_results': results['scanner_results']
#         })
#     except Exception as e:
#         logger.error(f"Error scanning prompt: {str(e)}")
#         return jsonify({'error': f'Scanning failed: {str(e)}'}), 500
#
# @app.route('/api/scan/batch', methods=['POST'])
# def scan_batch():
#     """Scan multiple prompts in batch"""
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#
#     prompts = data.get('prompts', [])
#     if not prompts or not isinstance(prompts, list):
#         return jsonify({'error': 'No prompts array provided'}), 400
#
#     results = []
#     start_time = time.time()
#
#     for i, prompt in enumerate(prompts):
#         try:
#             sanitized_prompt, is_valid, scan_results = firewall.scan_prompt(prompt)
#             results.append({
#                 'index': i,
#                 'original_prompt': prompt,
#                 'sanitized_prompt': sanitized_prompt,
#                 'is_valid': is_valid,
#                 'risk_score': scan_results['total_risk_score'],
#                 'processing_time_ms': scan_results['total_processing_time'] * 1000,
#                 'scanner_results': scan_results['scanner_results']
#             })
#         except Exception as e:
#             results.append({
#                 'index': i,
#                 'original_prompt': prompt,
#                 'error': str(e),
#                 'is_valid': False,
#                 'risk_score': 1.0
#             })
#
#     total_time = time.time() - start_time
#     valid_count = sum(1 for r in results if r.get('is_valid', False))
#
#     return jsonify({
#         'total_prompts': len(prompts),
#         'valid_prompts': valid_count,
#         'invalid_prompts': len(prompts) - valid_count,
#         'total_processing_time_ms': total_time * 1000,
#         'results': results
#     })
#
# @app.route('/api/stats', methods=['GET'])
# def get_stats():
#     """Get firewall statistics"""
#     enabled_scanners = {name: config for name, config in firewall.get_scanner_configs().items()
#                        if config['enabled']}
#
#     return jsonify({
#         'total_scanners': len(firewall.scanner_configs),
#         'enabled_scanners': len(enabled_scanners),
#         'disabled_scanners': len(firewall.scanner_configs) - len(enabled_scanners),
#         'scanner_list': list(enabled_scanners.keys()),
#         'version': '1.0.0'
#     })

