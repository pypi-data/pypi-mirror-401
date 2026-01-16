"""
AI-Powered Safety Validation for CCE Deep Agent

This module implements command safety validation using AI to detect
prompt injection attempts and malicious commands, based on open-swe-v2 patterns.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ThreatType(Enum):
    """Types of security threats."""

    SAFE = "SAFE"
    PROMPT_INJECTION = "PROMPT_INJECTION"
    MALICIOUS_COMMAND = "MALICIOUS_COMMAND"
    SUSPICIOUS_PATTERN = "SUSPICIOUS_PATTERN"


class CommandSafetyValidation(BaseModel):
    """Result of command safety validation."""

    is_safe: bool = Field(description="Whether the command is safe to execute")
    threat_type: ThreatType = Field(description="Type of threat detected")
    reasoning: str = Field(description="Explanation of the safety assessment")
    detected_patterns: list[str] = Field(default_factory=list, description="Specific patterns detected")
    confidence: float = Field(default=0.0, description="Confidence score (0.0 to 1.0)")
    recommendations: list[str] = Field(default_factory=list, description="Safety recommendations")


@dataclass
class SafetyPattern:
    """Safety pattern for command validation."""

    name: str
    pattern: str
    threat_type: ThreatType
    description: str
    severity: int  # 1-5, where 5 is most severe


class CommandSafetyValidator:
    """
    AI-powered command safety validator.

    This class validates shell commands and code editing operations
    for safety, focusing on prompt injection detection and malicious command prevention.
    """

    def __init__(self):
        self.safety_patterns = self._initialize_safety_patterns()
        self.whitelist_patterns = self._initialize_whitelist_patterns()

    def _initialize_safety_patterns(self) -> list[SafetyPattern]:
        """Initialize safety patterns for threat detection."""
        return [
            # Prompt injection patterns
            SafetyPattern(
                name="prompt_injection_ignore",
                pattern=r"ignore\s+(previous|above|all)\s+(instructions?|prompts?|commands?)",
                threat_type=ThreatType.PROMPT_INJECTION,
                description="Attempt to ignore previous instructions",
                severity=5,
            ),
            SafetyPattern(
                name="prompt_injection_system",
                pattern=r"you\s+are\s+now\s+(a\s+)?(different|new|other)",
                threat_type=ThreatType.PROMPT_INJECTION,
                description="Attempt to change agent identity",
                severity=5,
            ),
            SafetyPattern(
                name="prompt_injection_override",
                pattern=r"override\s+(safety|security|protections?)",
                threat_type=ThreatType.PROMPT_INJECTION,
                description="Attempt to override safety measures",
                severity=5,
            ),
            SafetyPattern(
                name="prompt_injection_roleplay",
                pattern=r"(pretend|act\s+as|roleplay)\s+(to\s+be\s+)?(a\s+)?(hacker|malicious|evil)",
                threat_type=ThreatType.PROMPT_INJECTION,
                description="Attempt to roleplay as malicious entity",
                severity=4,
            ),
            # Malicious command patterns
            SafetyPattern(
                name="malicious_rm",
                pattern=r"rm\s+-rf\s+/(?!tmp|var/tmp)",
                threat_type=ThreatType.MALICIOUS_COMMAND,
                description="Dangerous recursive deletion outside safe directories",
                severity=5,
            ),
            SafetyPattern(
                name="malicious_format",
                pattern=r"(format|mkfs|dd\s+if=/dev/zero)",
                threat_type=ThreatType.MALICIOUS_COMMAND,
                description="Disk formatting commands",
                severity=5,
            ),
            SafetyPattern(
                name="malicious_network",
                pattern=r"(nc|netcat|telnet|ssh)\s+.*\s+(\d{1,3}\.){3}\d{1,3}",
                threat_type=ThreatType.MALICIOUS_COMMAND,
                description="Suspicious network connections",
                severity=4,
            ),
            SafetyPattern(
                name="malicious_sudo",
                pattern=r"sudo\s+(rm|format|mkfs|dd|shutdown|reboot)",
                threat_type=ThreatType.MALICIOUS_COMMAND,
                description="Dangerous sudo commands",
                severity=5,
            ),
            # Suspicious patterns
            SafetyPattern(
                name="suspicious_curl",
                pattern=r"curl\s+.*\|\s*sh",
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                description="Download and execute pattern",
                severity=3,
            ),
            SafetyPattern(
                name="suspicious_wget",
                pattern=r"wget\s+.*\|\s*sh",
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                description="Download and execute pattern",
                severity=3,
            ),
            SafetyPattern(
                name="suspicious_base64",
                pattern=r"echo\s+[A-Za-z0-9+/=]+\s*\|\s*base64\s+-d\s*\|\s*sh",
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                description="Base64 encoded command execution",
                severity=4,
            ),
        ]

    def _initialize_whitelist_patterns(self) -> list[str]:
        """Initialize whitelist patterns for safe commands."""
        return [
            r"ls\s+.*",
            r"cat\s+.*",
            r"grep\s+.*",
            r"find\s+.*",
            r"pwd",
            r"whoami",
            r"date",
            r"echo\s+.*",
            r"mkdir\s+.*",
            r"touch\s+.*",
            r"cp\s+.*",
            r"mv\s+.*",
            r"chmod\s+.*",
            r"chown\s+.*",
            r"git\s+.*",
            r"npm\s+.*",
            r"pip\s+.*",
            r"python\s+.*",
            r"node\s+.*",
        ]

    async def validate_command_safety(
        self, command: str, context: dict[str, Any] | None = None
    ) -> CommandSafetyValidation:
        """
        Validate if a shell command is safe to execute.

        Args:
            command: The command to validate
            context: Optional context information

        Returns:
            CommandSafetyValidation result
        """
        try:
            # Normalize command
            normalized_command = command.strip().lower()

            # Check whitelist first
            if self._is_whitelisted(normalized_command):
                return CommandSafetyValidation(
                    is_safe=True,
                    threat_type=ThreatType.SAFE,
                    reasoning="Command matches whitelist pattern",
                    confidence=0.9,
                )

            # Check for safety patterns
            detected_threats = []
            max_severity = 0

            for pattern in self.safety_patterns:
                if re.search(pattern.pattern, normalized_command, re.IGNORECASE):
                    detected_threats.append(
                        {
                            "pattern": pattern.name,
                            "description": pattern.description,
                            "severity": pattern.severity,
                            "threat_type": pattern.threat_type,
                        }
                    )
                    max_severity = max(max_severity, pattern.severity)

            # Determine overall safety
            if detected_threats:
                # Get the most severe threat
                primary_threat = max(detected_threats, key=lambda x: x["severity"])

                return CommandSafetyValidation(
                    is_safe=False,
                    threat_type=primary_threat["threat_type"],
                    reasoning=f"Detected {primary_threat['description']} (severity: {primary_threat['severity']}/5)",
                    detected_patterns=[t["pattern"] for t in detected_threats],
                    confidence=min(0.9, 0.5 + (max_severity * 0.1)),
                    recommendations=self._get_safety_recommendations(detected_threats),
                )
            else:
                # No threats detected, but not whitelisted
                return CommandSafetyValidation(
                    is_safe=True,
                    threat_type=ThreatType.SAFE,
                    reasoning="No safety threats detected, but command not in whitelist",
                    confidence=0.6,
                    recommendations=["Review command before execution", "Consider adding to whitelist if safe"],
                )

        except Exception as e:
            logger.error(f"Error validating command safety: {e}")
            return CommandSafetyValidation(
                is_safe=False,
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                reasoning=f"Error during validation: {str(e)}",
                confidence=0.0,
                recommendations=["Manual review required due to validation error"],
            )

    def _is_whitelisted(self, command: str) -> bool:
        """Check if command matches whitelist patterns."""
        for pattern in self.whitelist_patterns:
            if re.match(pattern, command):
                return True
        return False

    def _get_safety_recommendations(self, threats: list[dict[str, Any]]) -> list[str]:
        """Get safety recommendations based on detected threats."""
        recommendations = []

        for threat in threats:
            if threat["threat_type"] == ThreatType.PROMPT_INJECTION:
                recommendations.append("Block command - potential prompt injection detected")
            elif threat["threat_type"] == ThreatType.MALICIOUS_COMMAND:
                recommendations.append("Block command - potentially destructive operation")
            elif threat["threat_type"] == ThreatType.SUSPICIOUS_PATTERN:
                recommendations.append("Review command - suspicious pattern detected")

        if not recommendations:
            recommendations.append("Manual review recommended")

        return list(set(recommendations))  # Remove duplicates

    async def validate_code_editing_safety(
        self, operation: str, file_path: str, content: str | None = None
    ) -> CommandSafetyValidation:
        """
        Validate code editing operations for safety.

        Args:
            operation: The editing operation (write_file, edit_file, etc.)
            file_path: Path to the file being edited
            content: Optional content being written

        Returns:
            CommandSafetyValidation result
        """
        try:
            # Check file path safety
            if self._is_dangerous_file_path(file_path):
                return CommandSafetyValidation(
                    is_safe=False,
                    threat_type=ThreatType.MALICIOUS_COMMAND,
                    reasoning=f"Dangerous file path: {file_path}",
                    confidence=0.9,
                    recommendations=["Block operation - dangerous file path"],
                )

            # Check content safety if provided
            if content:
                content_validation = await self.validate_command_safety(content)
                if not content_validation.is_safe:
                    return CommandSafetyValidation(
                        is_safe=False,
                        threat_type=content_validation.threat_type,
                        reasoning=f"Unsafe content detected: {content_validation.reasoning}",
                        detected_patterns=content_validation.detected_patterns,
                        confidence=content_validation.confidence,
                        recommendations=content_validation.recommendations,
                    )

            return CommandSafetyValidation(
                is_safe=True,
                threat_type=ThreatType.SAFE,
                reasoning="Code editing operation appears safe",
                confidence=0.8,
            )

        except Exception as e:
            logger.error(f"Error validating code editing safety: {e}")
            return CommandSafetyValidation(
                is_safe=False,
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                reasoning=f"Error during validation: {str(e)}",
                confidence=0.0,
                recommendations=["Manual review required due to validation error"],
            )

    def _is_dangerous_file_path(self, file_path: str) -> bool:
        """Check if file path is dangerous."""
        dangerous_paths = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/sudoers",
            "/boot/",
            "/sys/",
            "/proc/",
            "/dev/",
            "/root/",
            "/usr/bin/",
            "/usr/sbin/",
            "/bin/",
            "/sbin/",
        ]

        normalized_path = file_path.strip()
        for dangerous_path in dangerous_paths:
            if normalized_path.startswith(dangerous_path):
                return True

        return False

    def get_safety_statistics(self) -> dict[str, Any]:
        """Get safety validation statistics."""
        return {
            "total_patterns": len(self.safety_patterns),
            "whitelist_patterns": len(self.whitelist_patterns),
            "threat_types": [t.value for t in ThreatType],
            "pattern_categories": {
                "prompt_injection": len(
                    [p for p in self.safety_patterns if p.threat_type == ThreatType.PROMPT_INJECTION]
                ),
                "malicious_command": len(
                    [p for p in self.safety_patterns if p.threat_type == ThreatType.MALICIOUS_COMMAND]
                ),
                "suspicious_pattern": len(
                    [p for p in self.safety_patterns if p.threat_type == ThreatType.SUSPICIOUS_PATTERN]
                ),
            },
        }


# Global safety validator instance (lazy initialization to avoid import side effects)
_safety_validator: CommandSafetyValidator | None = None


def get_safety_validator() -> CommandSafetyValidator:
    """Get the global safety validator instance (lazy initialized)."""
    global _safety_validator
    if _safety_validator is None:
        _safety_validator = CommandSafetyValidator()
    return _safety_validator


async def validate_command_safety(command: str, context: dict[str, Any] | None = None) -> CommandSafetyValidation:
    """
    Validate if a shell command is safe to execute.

    Args:
        command: The command to validate
        context: Optional context information

    Returns:
        CommandSafetyValidation result
    """
    return await get_safety_validator().validate_command_safety(command, context)


async def validate_code_editing_safety(
    operation: str, file_path: str, content: str | None = None
) -> CommandSafetyValidation:
    """
    Validate code editing operations for safety.

    Args:
        operation: The editing operation
        file_path: Path to the file being edited
        content: Optional content being written

    Returns:
        CommandSafetyValidation result
    """
    return await get_safety_validator().validate_code_editing_safety(operation, file_path, content)
