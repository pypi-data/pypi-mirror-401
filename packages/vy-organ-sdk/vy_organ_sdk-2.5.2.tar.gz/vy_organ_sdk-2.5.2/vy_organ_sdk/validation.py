import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    pass


class ManifestValidator:
    def __init__(self, manifest_path: str = "manifest.json"):
        self.manifest_path = Path(manifest_path)
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")

        with open(self.manifest_path) as f:
            self.manifest = json.load(f)

        self._validate_manifest_structure()

    def _validate_manifest_structure(self):
        required_fields = ["manifest_version", "organ_id", "intents"]

        for field in required_fields:
            if field not in self.manifest:
                raise ValidationError(f"Missing required field: {field}")

        if self.manifest["manifest_version"] not in ("2", "3"):
            raise ValidationError(
                f"Unsupported manifest version: {self.manifest['manifest_version']}. "
                "Expected '2' or '3'"
            )

        if not isinstance(self.manifest["intents"], dict):
            raise ValidationError("'intents' must be a dictionary")

        if not self.manifest["intents"]:
            raise ValidationError("Manifest must declare at least one intent")

        logger.debug(f"Manifest structure valid: {self.manifest['organ_id']}")

    def validate_intent_schemas(self):
        for intent_name, intent_spec in self.manifest["intents"].items():
            if not isinstance(intent_spec, dict):
                raise ValidationError(f"Intent '{intent_name}' spec must be a dictionary")

            required_spec_fields = ["timeout_ms", "idempotent"]
            for field in required_spec_fields:
                if field not in intent_spec:
                    logger.warning(f"Intent '{intent_name}' missing recommended field: {field}")

            if "input_schema" in intent_spec:
                if not isinstance(intent_spec["input_schema"], dict):
                    raise ValidationError(
                        f"Intent '{intent_name}' input_schema must be a dictionary"
                    )

            if "output_schema" in intent_spec:
                if not isinstance(intent_spec["output_schema"], dict):
                    raise ValidationError(
                        f"Intent '{intent_name}' output_schema must be a dictionary"
                    )

        logger.debug(f"All {len(self.manifest['intents'])} intent schemas valid")

    def get_declared_intents(self) -> Set[str]:
        
        return set(self.manifest["intents"].keys())

    def get_intent_spec(self, intent_name: str) -> Optional[Dict[str, Any]]:
        return self.manifest["intents"].get(intent_name)

    def get_organ_id(self) -> str:
        return self.manifest["organ_id"]

    def get_organ_version(self) -> str:
        return self.manifest.get("version", "1.0.0")


def validate_handler_against_manifest(
    handler_intents: List[str],
    manifest_path: str = "manifest.json",
    strict: bool = True
) -> ManifestValidator:
    validator = ManifestValidator(manifest_path)
    validator.validate_intent_schemas()

    handler_set = set(handler_intents)
    manifest_set = validator.get_declared_intents()

    missing_in_handler = manifest_set - handler_set
    extra_in_handler = handler_set - manifest_set

    errors = []

    if missing_in_handler:
        msg = (
            f"Handler missing intents declared in manifest: {missing_in_handler}\n"
            f"  Manifest declares: {sorted(manifest_set)}\n"
            f"  Handler implements: {sorted(handler_set)}\n"
            f"  Add these intents to handler.supported_intents"
        )
        errors.append(msg)

    if extra_in_handler:
        msg = (
            f"Handler implements intents not in manifest: {extra_in_handler}\n"
            f"  Manifest declares: {sorted(manifest_set)}\n"
            f"  Handler implements: {sorted(handler_set)}\n"
            f"  Either add to manifest or remove from handler"
        )
        errors.append(msg)

    if errors:
        full_error = "\n\n".join(errors)
        if strict:
            logger.error(f"Validation failed:\n{full_error}")
            raise ValidationError(full_error)
        else:
            logger.warning(f"Validation warnings:\n{full_error}")
    else:
        logger.info(
            f"✅ Handler validation passed: {len(handler_set)} intents match manifest"
        )

    return validator


def auto_load_intents_from_manifest(manifest_path: str = "manifest.json") -> List[str]:
    validator = ManifestValidator(manifest_path)
    intents = sorted(validator.get_declared_intents())
    logger.debug(f"Auto-loaded {len(intents)} intents from {manifest_path}")
    return intents


def validate_payload_against_schema(
    payload: Dict[str, Any],
    schema: Dict[str, Any],
    intent_name: str
) -> bool:
    if not schema:
        return True

    required_fields = schema.get("required", [])

    for field in required_fields:
        if field not in payload:
            raise ValidationError(
                f"Intent '{intent_name}': Missing required field '{field}' in payload"
            )

    properties = schema.get("properties", {})

    for field_name, field_value in payload.items():
        if field_name not in properties:
            logger.warning(
                f"Intent '{intent_name}': Unexpected field '{field_name}' in payload"
            )

    return True