"""Batch validation error classes for ML model data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from arize.constants.ml import (
    MAX_EMBEDDING_DIMENSIONALITY,
    MAX_FUTURE_YEARS_FROM_CURRENT_TIME,
    MAX_MULTI_CLASS_NAME_LENGTH,
    MAX_NUMBER_OF_EMBEDDINGS,
    MAX_NUMBER_OF_MULTI_CLASS_CLASSES,
    MAX_PAST_YEARS_FROM_CURRENT_TIME,
    MAX_RAW_DATA_CHARACTERS,
    MAX_TAG_LENGTH,
)
from arize.logging import log_a_list
from arize.types import Environments, ModelTypes

if TYPE_CHECKING:
    from collections.abc import Iterable

    from arize.types import Metrics


class ValidationError(Exception, ABC):
    """Base class for validation errors during batch data ingestion."""

    def __str__(self) -> str:
        """Return a human-readable error message."""
        return self.error_message()

    @abstractmethod
    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""

    @abstractmethod
    def error_message(self) -> str:
        """Return the error message for this exception."""


class ValidationFailure(Exception):
    """Raised when validation encounters multiple errors during processing."""

    def __init__(self, errors: list[ValidationError]) -> None:
        """Initialize the exception with a list of validation errors.

        Args:
            errors: List of validation errors encountered during processing.
        """
        self.errors = errors


# ----------------------
# Minimum required checks
# ----------------------
class InvalidColumnNameEmptyString(ValidationError):
    """Raised when a schema contains an empty string as a column name."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Column_Name_Empty_String"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Empty column name found: ''. The schema cannot point to columns in the "
            "dataframe denoted by an empty string. You can see the columns used in the "
            "schema by running schema.get_used_columns()"
        )


class InvalidFieldTypeConversion(ValidationError):
    """Raised when field values cannot be converted to the required type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Input_Type_Conversion"

    def __init__(self, fields: Iterable, type: str) -> None:
        """Initialize the exception with field type conversion context.

        Args:
            fields: Fields that failed type conversion.
            type: Expected type for the fields.
        """
        self.fields = fields
        self.type = type

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"The following fields must be convertible to {self.type}: "
            f"{', '.join(map(str, self.fields))}."
        )


class InvalidFieldTypeEmbeddingFeatures(ValidationError):
    """Raised when embedding feature column names are not properly formatted."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Input_Type_Embedding_Features"

    def __init__(self) -> None:
        """Initialize the exception."""

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "schema.embedding_feature_column_names should be a dictionary mapping strings "
            "to EmbeddingColumnNames objects"
        )


class InvalidFieldTypePromptResponse(ValidationError):
    """Raised when prompt response field is not of correct type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Input_Type_Prompt_Response"

    def __init__(self, name: str) -> None:
        """Initialize the exception with field name context.

        Args:
            name: Name of the field with invalid prompt response type.
        """
        self.name = name

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return f"'{self.name}' must be of type str or EmbeddingColumnNames"


class InvalidDataFrameIndex(ValidationError):
    """Raised when the dataframe index is invalid and needs to be reset."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Index"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The index of the dataframe is invalid; "
            "reset the index by using df.reset_index(drop=True, inplace=True)"
        )


class InvalidSchemaType(ValidationError):
    """Raised when schema type is incompatible with the model environment."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Schema_Type"

    def __init__(self, schema_type: str, environment: Environments) -> None:
        """Initialize the exception with schema type and environment context.

        Args:
            schema_type: Type of schema that is invalid.
            environment: Model environment where schema is being used.
        """
        self.schema_type = schema_type
        self.environment = environment

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return f"Cannot use a {self.schema_type} for a model with environment: {self.environment}"


# ----------------
# Parameter checks
# ----------------


class MissingPredictionIdColumnForDelayedRecords(ValidationError):
    """Raised when prediction ID is missing for delayed actuals or feature importance."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Prediction_Id_Column_For_Delayed_Records"

    def __init__(
        self, has_actual_info: bool, has_feature_importance_info: bool
    ) -> None:
        """Initialize the exception with delayed record context.

        Args:
            has_actual_info: Whether actual information is present.
            has_feature_importance_info: Whether feature importance information is present.
        """
        self.has_actual_info = has_actual_info
        self.has_feature_importance_info = has_feature_importance_info

    def error_message(self) -> str:
        """Return the error message for this exception."""
        actual = "actual" if self.has_actual_info else ""
        feat_imp = (
            "feature importance" if self.has_feature_importance_info else ""
        )
        if self.has_actual_info and self.has_feature_importance_info:
            msg = " and ".join([actual, feat_imp])
        else:
            msg = "".join([actual, feat_imp])

        return (
            "Missing 'prediction_id_column_name'. While prediction id is optional for most cases, "
            "it is required when sending delayed actuals, i.e. when sending actual or feature importances "
            f"without predictions. In this case, {msg} information was found (without predictions). "
            "To learn more about delayed joins, please see the docs at "
            "https://docs.arize.com/arize/sending-data-guides/how-to-send-delayed-actuals"
        )


class MissingColumns(ValidationError):
    """Raised when columns declared in schema are not found in dataframe."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Columns"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with missing columns context.

        Args:
            cols: Columns declared in schema but not found in dataframe.
        """
        self.missing_cols = set(cols)

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The following columns are declared in the schema "
            "but are not found in the dataframe: "
            f"{', '.join(map(str, self.missing_cols))}."
        )


class MissingRequiredColumnsMetricsValidation(ValidationError):
    """This error is used only for model mapping validations."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Columns_Required_By_Metrics_Validation"

    def __init__(
        self, model_type: ModelTypes, metrics: list[Metrics], cols: Iterable
    ) -> None:
        """Initialize the exception with model metrics validation context.

        Args:
            model_type: Type of model being validated.
            metrics: List of metrics requiring validation.
            cols: Required columns that are missing.
        """
        self.model_type = model_type
        self.metrics = metrics
        self.missing_cols = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"For logging data for a {self.model_type.name} model with support for metrics "
            f"{', '.join(m.name for m in self.metrics)}, "
            f"schema must include: {', '.join(map(str, self.missing_cols))}."
        )


class ReservedColumns(ValidationError):
    """Raised when reserved column names are used in schema fields."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Reserved_Columns"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with reserved columns context.

        Args:
            cols: Reserved columns that cannot be used in schema fields.
        """
        self.reserved_columns = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The following columns are reserved and can only be specified "
            "in the proper fields of the schema: "
            f"{', '.join(map(str, self.reserved_columns))}."
        )


class InvalidModelTypeAndMetricsCombination(ValidationError):
    """This error is used only for model mapping validations."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_ModelType_And_Metrics_Combination"

    def __init__(
        self,
        model_type: ModelTypes,
        metrics: list[Metrics],
        suggested_model_metric_combinations: list[list[str]],
    ) -> None:
        """Initialize the exception with model type and metrics combination context.

        Args:
            model_type: Type of model being validated.
            metrics: List of metrics that form invalid combination with model type.
            suggested_model_metric_combinations: Valid metric combinations for the model type.
        """
        self.model_type = model_type
        self.metrics = metrics
        self.suggested_combinations = suggested_model_metric_combinations

    def error_message(self) -> str:
        """Return the error message for this exception."""
        valid_combos = ", or \n".join(
            "[" + ", ".join(combo) + "]"
            for combo in self.suggested_combinations
        )
        return (
            f"Invalid combination of model type {self.model_type.name} and metrics: "
            f"{', '.join(m.name for m in self.metrics)}. "
            f"Valid Metric combinations for this model type:\n{valid_combos}.\n"
        )


class InvalidShapSuffix(ValidationError):
    """Raised when feature or tag names use the reserved '_shap' suffix."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_SHAP_Suffix"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with invalid SHAP suffix columns.

        Args:
            cols: Feature or tag columns using the reserved '_shap' suffix.
        """
        self.invalid_column_names = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The following features or tags must not be named with a `_shap` suffix: "
            f"{', '.join(map(str, self.invalid_column_names))}."
        )


class InvalidModelType(ValidationError):
    """Raised when an invalid model type is specified."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Model_Type"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Model type not valid. Choose one of the following: "
            f"{', '.join('ModelTypes.' + mt.name for mt in ModelTypes)}. "
        )


class InvalidEnvironment(ValidationError):
    """Raised when an invalid environment is specified."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Environment"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Environment not valid. Choose one of the following: "
            f"{', '.join('Environments.' + env.name for env in Environments)}. "
        )


class InvalidBatchId(ValidationError):
    """Raised when batch ID is missing or invalid for validation environment."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Batch_ID"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "Batch ID must be a nonempty string if logging to validation environment."


class InvalidModelVersion(ValidationError):
    """Raised when model version is empty or invalid."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Model_Version"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "Model version must be a nonempty string."


class InvalidModelId(ValidationError):
    """Raised when model ID is empty or invalid."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Model_ID"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "Model ID must be a nonempty string."


class InvalidProjectName(ValidationError):
    """Raised when project name is empty or invalid."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Project_Name"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Project Name must be a nonempty string. "
            "If Model ID was used instead of Project Name, "
            "it must be a nonempty string."
        )


class MissingPredActShap(ValidationError):
    """Raised when schema is missing prediction, actual, or SHAP values."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Pred_or_Act_or_SHAP"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The schema must specify at least one of the following: "
            "prediction label, actual label, or SHAP value column names"
        )


class MissingPreprodPredAct(ValidationError):
    """Raised when pre-production data is missing both prediction and actual labels."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Preproduction_Pred_and_Act"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "For logging pre-production data, the schema must specify both "
            "prediction and actual label columns."
        )


class MissingPreprodAct(ValidationError):
    """Raised when pre-production data is missing actual label column."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Preproduction_Act"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "For logging pre-production data, the schema must specify actual label column."


class MissingPreprodPredActNumericAndCategorical(ValidationError):
    """Raised when pre-production numeric/categorical model is missing prediction or actual columns."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Preproduction_Pred_and_Act_Numeric_and_Categorical"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "For logging pre-production data for a numeric or a categorical model, "
            "the schema must specify both prediction and actual label or score columns."
        )


class MissingRequiredColumnsForRankingModel(ValidationError):
    """Raised when ranking model is missing required group ID or rank columns."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Required_Columns_For_Ranking_Model"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "For logging data for a ranking model, schema must specify: "
            "prediction_group_id_column_name and rank_column_name"
        )


class MissingCVPredAct(ValidationError):
    """Raised when computer vision model is missing prediction or actual columns."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_CV_Prediction_or_Actual"

    def __init__(self, environment: Environments) -> None:
        """Initialize the exception with environment context.

        Args:
            environment: Model environment (training, validation, or production).
        """
        self.environment = environment

    def error_message(self) -> str:
        """Return the error message for this exception."""
        if self.environment in (Environments.TRAINING, Environments.VALIDATION):
            env = "pre-production"
            opt = "and"
        elif self.environment == Environments.PRODUCTION:
            env = "production"
            opt = "or"
        else:
            raise TypeError("Invalid environment")
        return (
            f"For logging {env} data for an Object Detection model, "
            "the schema must specify one of: "
            f"('object_detection_prediction_column_names' {opt} "
            f"'object_detection_actual_column_names') "
            f"or ('semantic_segmentation_prediction_column_names' {opt} "
            f"'semantic_segmentation_actual_column_names') "
            f"or ('instance_segmentation_prediction_column_names' {opt} "
            f"'instance_segmentation_actual_column_names')"
        )


class MultipleCVPredAct(ValidationError):
    """Raised when multiple computer vision prediction/actual types are specified."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Multiple_CV_Prediction_or_Actual"

    def __init__(self, environment: Environments) -> None:
        """Initialize the exception with environment context.

        Args:
            environment: Model environment where multiple CV types were specified.
        """
        self.environment = environment

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The schema must only specify one of the following: "
            "'object_detection_prediction_column_names'/'object_detection_actual_column_names', "
            "'semantic_segmentation_prediction_column_names'/'semantic_segmentation_actual_column_names', "
            "'instance_segmentation_prediction_column_names'/'instance_segmentation_actual_column_names'."
        )


class InvalidPredActCVColumnNamesForModelType(ValidationError):
    """Raised when CV columns are used for non-OBJECT_DETECTION model types."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_CV_Prediction_or_Actual_Column_Names_for_Model_Type"

    def __init__(
        self,
        invalid_model_type: ModelTypes,
    ) -> None:
        """Initialize the exception with model type context.

        Args:
            invalid_model_type: Model type that cannot use CV columns.
        """
        self.invalid_model_type = invalid_model_type

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Cannot use 'object_detection_prediction_column_names' or "
            f"'object_detection_actual_column_names' or "
            f"'semantic_segmentation_prediction_column_names' or "
            f"'semantic_segmentation_actual_column_names' or "
            f"'instance_segmentation_prediction_column_names' or "
            f"'instance_segmentation_actual_column_names' for {self.invalid_model_type} model "
            f"type. They are only allowed for ModelTypes.OBJECT_DETECTION models"
        )


class MissingReqPredActColumnNamesForMultiClass(ValidationError):
    """Raised when multi-class model is missing required score columns."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Missing_Required_Prediction_or_Actual_Column_Names_for_Multi_Class_Model_Type"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "For logging data for a multi class model, schema must specify: "
            "prediction_scores_column_name and/or actual_score_column_name. "
            "Optionally, you may include multi_class_threshold_scores_column_name "
            "(must include prediction_scores_column_name)"
        )


class InvalidPredActColumnNamesForModelType(ValidationError):
    """Raised when prediction/actual columns are invalid for the model type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Prediction_or_Actual_Column_Names_for_Model_Type"

    def __init__(
        self,
        invalid_model_type: ModelTypes,
        allowed_fields: list[str],
        wrong_columns: list[str],
    ) -> None:
        """Initialize the exception with model type and column validation context.

        Args:
            invalid_model_type: Model type with invalid columns.
            allowed_fields: List of allowed schema fields for the model type.
            wrong_columns: Columns that are invalid for the model type.
        """
        self.invalid_model_type = invalid_model_type
        self.allowed_fields = allowed_fields
        self.wrong_columns = wrong_columns

    def error_message(self) -> str:
        """Return the error message for this exception."""
        allowed_col_msg = ""
        if self.allowed_fields is not None:
            allowed_col_msg = f" Allowed Schema fields are {log_a_list(self.allowed_fields, 'and')}"
        return (
            f"Invalid Schema fields for {self.invalid_model_type} model type. {allowed_col_msg}. "
            "The following columns of your dataframe are sent as an invalid schema field: "
            f"{log_a_list(self.wrong_columns, 'and')}"
        )


class DuplicateColumnsInDataframe(ValidationError):
    """Raised when dataframe contains duplicate column names used in schema."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Duplicate_Columns_In_Dataframe"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with duplicate columns context.

        Args:
            cols: Columns that have duplicates in the dataframe.
        """
        self.duplicate_cols = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "The following columns are present in the schema and have duplicates in the dataframe: "
            f"{self.duplicate_cols}. "
        )


class InvalidNumberOfEmbeddings(ValidationError):
    """Raised when the number of embeddings exceeds the maximum allowed."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Number_Of_Embeddings"

    def __init__(self, number_of_embeddings: int) -> None:
        """Initialize the exception with embedding count context.

        Args:
            number_of_embeddings: Number of embeddings found in the schema.
        """
        self.number_of_embeddings = number_of_embeddings

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"The schema contains {self.number_of_embeddings} different embeddings when a maximum of "
            f"{MAX_NUMBER_OF_EMBEDDINGS} is allowed."
        )


# -----------
# Type checks
# -----------


class InvalidType(ValidationError):
    """Raised when a field has an invalid data type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Type"

    def __init__(
        self, name: str, expected_types: list[str], found_data_type: str
    ) -> None:
        """Initialize the exception with type validation context.

        Args:
            name: Name of the field with invalid type.
            expected_types: List of expected data types.
            found_data_type: Actual data type found.
        """
        self.name = name
        self.expected_types = expected_types
        self.found_data_type = found_data_type

    def error_message(self) -> str:
        """Return the error message for this exception."""
        type_list = (
            self.expected_types[0]
            if len(self.expected_types) == 1
            else f"{', '.join(map(str, self.expected_types[:-1]))} or {self.expected_types[-1]}"
        )
        return (
            f"{self.name} must be of type {type_list} but found {self.found_data_type}. "
            "Warning: if you are sending a column with integers, presence of a null "
            "value can convert the data type of the entire column to float."
        )


class InvalidTypeColumns(ValidationError):
    """Raised when columns have invalid data types."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Type_Columns"

    def __init__(
        self, wrong_type_columns: list[str], expected_types: list[str]
    ) -> None:
        """Initialize the exception with column type validation context.

        Args:
            wrong_type_columns: Columns with incorrect data types.
            expected_types: List of expected data types for the columns.
        """
        self.wrong_type_columns = wrong_type_columns
        self.expected_types = expected_types

    def error_message(self) -> str:
        """Return the error message for this exception."""
        col_list = (
            self.wrong_type_columns[0]
            if len(self.wrong_type_columns) == 1
            else f"{', '.join(self.wrong_type_columns[:-1])}, and {self.wrong_type_columns[-1]}"
        )
        type_list = (
            self.expected_types[0]
            if len(self.expected_types) == 1
            else f"{', '.join(map(str, self.expected_types[:-1]))} or {self.expected_types[-1]}"
        )
        return f"The column(s) {col_list}; must be of type {type_list}."


class InvalidTypeFeatures(ValidationError):
    """Raised when feature columns have unrecognized data types."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Type_Features"

    def __init__(self, cols: Iterable, expected_types: list[str]) -> None:
        """Initialize the exception with feature type validation context.

        Args:
            cols: Feature columns with unrecognized data types.
            expected_types: List of expected data types for features.
        """
        self.wrong_type_columns = cols
        self.expected_types = expected_types

    def error_message(self) -> str:
        """Return the error message for this exception."""
        type_list = (
            self.expected_types[0]
            if len(self.expected_types) == 1
            else f"{', '.join(map(str, self.expected_types[:-1]))} or {self.expected_types[-1]}"
        )
        return (
            f"Features must be of type {type_list}. "
            "The following feature columns have unrecognized data types: "
            f"{', '.join(map(str, self.wrong_type_columns))}."
        )


class InvalidFieldTypePromptTemplates(ValidationError):
    """Raised when prompt template column names are not of correct type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Input_Type_Prompt_Templates"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "prompt_template_column_names must be of type PromptTemplateColumnNames"


class InvalidFieldTypeLlmConfig(ValidationError):
    """Raised when LLM config column names are not of correct type."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Input_Type_LLM_Config"

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return "llm_config_column_names must be of type LLMConfigColumnNames"


class InvalidTypeTags(ValidationError):
    """Raised when tag columns have unrecognized data types."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Type_Tags"

    def __init__(self, cols: Iterable, expected_types: list[str]) -> None:
        """Initialize the exception with tag type validation context.

        Args:
            cols: Tag columns with unrecognized data types.
            expected_types: List of expected data types for tags.
        """
        self.wrong_type_columns = cols
        self.expected_types = expected_types

    def error_message(self) -> str:
        """Return the error message for this exception."""
        type_list = (
            self.expected_types[0]
            if len(self.expected_types) == 1
            else f"{', '.join(map(str, self.expected_types[:-1]))} or {self.expected_types[-1]}"
        )
        return (
            f"Tags must be of type {type_list}. "
            "The following tag columns have unrecognized data types: "
            f"{', '.join(map(str, self.wrong_type_columns))}."
        )


class InvalidValueEmbeddingVectorDimensionality(ValidationError):
    """Raised when embedding vector dimensionality is out of valid range."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Value_Embedding_Vector_Dimensionality"

    def __init__(self, dim_1_cols: list[str], high_dim_cols: list[str]) -> None:
        """Initialize the exception with embedding dimensionality context.

        Args:
            dim_1_cols: Columns with dimensionality of 1.
            high_dim_cols: Columns with dimensionality exceeding the maximum.
        """
        self.dim_1_cols = dim_1_cols
        self.high_dim_cols = high_dim_cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = (
            "Embedding vectors cannot have length (dimensionality) of 1 or higher "
            f"than {MAX_EMBEDDING_DIMENSIONALITY}. "
        )
        if self.dim_1_cols:
            msg += f"The following columns have dimensionality of 1: {','.join(self.dim_1_cols)}. "
        if self.high_dim_cols:
            msg += (
                f"The following columns have dimensionality greater than {MAX_EMBEDDING_DIMENSIONALITY}: "
                f"{','.join(self.high_dim_cols)}. "
            )

        return msg


class InvalidValueEmbeddingRawDataTooLong(ValidationError):
    """Raised when embedding raw data exceeds maximum character limit."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Value_Embedding_Raw_Data_Too_Long"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with raw data length validation context.

        Args:
            cols: Columns with embedding raw data exceeding maximum characters.
        """
        self.invalid_cols = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Embedding raw data cannot have more than {MAX_RAW_DATA_CHARACTERS} characters. "
            "The following columns do not satisfy this condition: "
            f"{', '.join(map(str, self.invalid_cols))}."
        )


class InvalidTypeShapValues(ValidationError):
    """Raised when SHAP value columns have unrecognized data types."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Type_SHAP_Values"

    def __init__(self, cols: Iterable, expected_types: list[str]) -> None:
        """Initialize the exception with SHAP value type validation context.

        Args:
            cols: SHAP value columns with unrecognized data types.
            expected_types: List of expected data types for SHAP values.
        """
        self.wrong_type_columns = cols
        self.expected_types = expected_types

    def error_message(self) -> str:
        """Return the error message for this exception."""
        type_list = (
            self.expected_types[0]
            if len(self.expected_types) == 1
            else f"{', '.join(map(str, self.expected_types[:-1]))} or {self.expected_types[-1]}"
        )
        return (
            f"SHAP values must be of type {type_list}. "
            "The following SHAP columns have unrecognized data types: "
            f"{', '.join(map(str, self.wrong_type_columns))}."
        )


# -----------
# Value checks
# -----------


class InvalidValueTimestamp(ValidationError):
    """Raised when timestamp values are outside acceptable time range."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Timestamp_Value"

    def __init__(self, timestamp_col_name: str) -> None:
        """Initialize the exception with timestamp validation context.

        Args:
            timestamp_col_name: Name of the column containing invalid timestamp values.
        """
        self.timestamp_col_name = timestamp_col_name

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Prediction timestamp in {self.timestamp_col_name} is out of range. "
            f"Prediction timestamps must be within {MAX_FUTURE_YEARS_FROM_CURRENT_TIME} year "
            f"in the future and {MAX_PAST_YEARS_FROM_CURRENT_TIME} years in the past from "
            "the current time. If this is your pre-production data, you could also just "
            "remove the timestamp column from the Schema."
        )


class InvalidValueMissingValue(ValidationError):
    """Raised when required fields contain null or missing values."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Missing_Value"

    def __init__(
        self, name: str, wrong_values: str, column: str | None = None
    ) -> None:
        """Initialize the exception with missing value validation context.

        Args:
            name: Name of the field with missing values.
            wrong_values: Description of the wrong values found (e.g., "null", "NaN").
            column: Optional column name where missing values were found.
        """
        self.name = name
        self.wrong_values = wrong_values
        self.column = column

    def error_message(self) -> str:
        """Return the error message for this exception."""
        if self.name in ["Prediction ID", "Prediction Group ID", "Rank"]:
            return f"{self.name} column '{self.column}' must not contain {self.wrong_values} values."
        return f"{self.name} must not contain {self.wrong_values} values."


class InvalidRankValue(ValidationError):
    """Raised when ranking column values are outside acceptable range."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Rank_Value"

    def __init__(self, name: str, acceptable_range: str) -> None:
        """Initialize the exception with rank validation context.

        Args:
            name: Name of the ranking column.
            acceptable_range: Description of the acceptable value range.
        """
        self.name = name
        self.acceptable_range = acceptable_range

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"ranking column {self.name} is out of range. "
            f"Only values within {self.acceptable_range} are accepted."
        )


class InvalidStringLengthInColumn(ValidationError):
    """Raised when string values in a column exceed length limits."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_String_Length_In_Column"

    def __init__(
        self, schema_name: str, col_name: str, min_length: int, max_length: int
    ) -> None:
        """Initialize the exception with string length validation context.

        Args:
            schema_name: Name of the schema field.
            col_name: Name of the column with invalid string lengths.
            min_length: Minimum acceptable string length.
            max_length: Maximum acceptable string length.
        """
        self.schema_name = schema_name
        self.col_name = col_name
        self.min_length = min_length
        self.max_length = max_length

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"{self.schema_name} column '{self.col_name}' contains invalid values. "
            f"Only string values of length between {self.min_length} and {self.max_length} are accepted."
        )


class InvalidTagLength(ValidationError):
    """Raised when tag values exceed maximum character length."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Tag_Length"

    def __init__(self, cols: Iterable) -> None:
        """Initialize the exception with tag length validation context.

        Args:
            cols: Tag columns with values exceeding maximum character length.
        """
        self.wrong_value_columns = cols

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Only tag values with less than or equal to {MAX_TAG_LENGTH} characters are supported. "
            f"The following tag columns have more than {MAX_TAG_LENGTH} characters: "
            f"{', '.join(map(str, self.wrong_value_columns))}."
        )


class InvalidRankingCategoryValue(ValidationError):
    """Raised when ranking relevance labels contain invalid values."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Ranking_Relevance_Labels_Value"

    def __init__(self, name: str) -> None:
        """Initialize the exception with ranking category validation context.

        Args:
            name: Name of the ranking relevance labels column.
        """
        self.name = name

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Ranking relevance labels '{self.name}' column contains invalid value. "
            f"Make sure empty string is not present"
        )


class InvalidBoundingBoxesCoordinates(ValidationError, Exception):
    """Raised when bounding box coordinates are invalid or incorrectly formatted."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Bounding_Boxes_Coordinates"

    def __init__(self, reason: str) -> None:
        """Initialize the exception with bounding box coordinate validation context.

        Args:
            reason: Specific reason for invalid coordinates (e.g., "none_boxes",
                "none_or_empty_box", "boxes_coordinates_wrong_format").
        """
        self._check_valid_reason(reason)
        self.reason = reason

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_boxes",
            "none_or_empty_box",
            "boxes_coordinates_wrong_format",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid bounding boxes coordinates found. "
        if self.reason == "none_boxes":
            msg += (
                "Found at least one list of bounding boxes coordinates with NoneType. List of "
                "bounding boxes coordinates cannot be None, if you'd like to send no boxes, "
                "send an empty list"
            )
        elif self.reason == "none_or_empty_box":
            msg += (
                "Found at least one bounding box with None value or without coordinates. All "
                "bounding boxes in the list must contain its 4 coordinates"
            )
        elif self.reason == "boxes_coordinates_wrong_format":
            msg += (
                "Found at least one bound box's coordinates incorrectly formatted. Each "
                "bounding box's coordinates must be a collection of 4 positive floats "
                "representing the top-left & bottom-right corners of the box, in pixels"
            )
        return msg


class InvalidBoundingBoxesCategories(ValidationError, Exception):
    """Raised when bounding box categories are invalid or missing."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Bounding_Boxes_Categories"

    def __init__(self, reason: str) -> None:
        """Initialize the exception with bounding box category validation context.

        Args:
            reason: Specific reason for invalid categories (e.g., "none_category_list",
                "none_category").
        """
        self._check_valid_reason(reason)
        self.reason = reason

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_category_list",
            "none_category",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid bounding boxes categories found. "
        if self.reason == "none_category_list":
            msg += (
                "Found at least one list of bounding box categories with None value. Must send a "
                "list of categories, one category per bounding box."
            )
        elif self.reason == "none_category":
            msg += (
                "Found at least one category label with None value. Each bounding box category "
                "must be string. Empty strings are allowed"
            )
        return msg


class InvalidBoundingBoxesScores(ValidationError, Exception):
    """Raised when bounding box confidence scores are invalid or out of bounds."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Bounding_Boxes_Scores"

    def __init__(self, reason: str) -> None:
        """Initialize the exception with bounding box score validation context.

        Args:
            reason: Specific reason for invalid scores (e.g., "none_score_list",
                "scores_out_of_bounds").
        """
        self._check_valid_reason(reason)
        self.reason = reason

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_score_list",
            "scores_out_of_bounds",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid bounding boxes scores found. "
        if self.reason == "none_score_list":
            msg += (
                "Found at least one list of bounding box scores with None value. This field is "
                "optional. If sent, you must send a confidence score per bounding box"
            )
        elif self.reason == "scores_out_of_bounds":
            msg += (
                "Found at least one confidence score out of bounds. "
                "Confidence scores must be between 0 and 1"
            )
        return msg


class InvalidPolygonCoordinates(ValidationError, Exception):
    """Raised when polygon coordinates are invalid or incorrectly formatted."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Polygon_Coordinates"

    def __init__(
        self, reason: str, coordinates: list[float] | None = None
    ) -> None:
        """Initialize the exception with polygon coordinate validation context.

        Args:
            reason: Specific reason for invalid coordinates (e.g., "none_polygons",
                "none_or_empty_polygon", "polygon_coordinates_wrong_format").
            coordinates: Optional list of invalid coordinates for error reporting.
        """
        self._check_valid_reason(reason)
        self.reason = reason
        self.coordinates = coordinates

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_polygons",
            "none_or_empty_polygon",
            "polygon_coordinates_wrong_format",
            "polygon_coordinates_repeated_vertices",
            "polygon_coordinates_self_intersecting_vertices",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid polygon coordinates found. "
        if self.reason == "none_polygons":
            msg += (
                "Found at least one list of polygon coordinates with NoneType. List of "
                "polygon coordinates cannot be None, if you'd like to send no coordinates, "
                "send an empty list"
            )
        elif self.reason == "none_or_empty_polygon":
            msg += (
                "Found at least one polygon with None value or without coordinates. All "
                "polygons in the list must contain its coordinates"
            )
        elif self.reason == "polygon_coordinates_wrong_format":
            msg += (
                "Found at least one polygon's coordinates incorrectly formatted. Each "
                "polygon's coordinates must be a collection of even number of positive floats "
                "representing the x and y coordinates of each point, in pixels. The following "
                f"coordinates are invalid: {self.coordinates}"
            )
        elif self.reason == "polygon_coordinates_repeated_vertices":
            msg += (
                "Found at least one polygon with repeated vertices. "
                "No polygon can have repeated vertices. "
                f"The following coordinates are invalid: {self.coordinates}"
            )
        elif self.reason == "polygon_coordinates_self_intersecting_vertices":
            msg += (
                "Found at least one polygon with self-intersecting vertices. "
                "Each polygon must not have self-intersecting vertices. "
                f"The following coordinates are invalid: {self.coordinates}"
            )
        return msg


class InvalidPolygonCategories(ValidationError, Exception):
    """Raised when polygon categories are invalid or missing."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Polygon_Categories"

    def __init__(self, reason: str) -> None:
        """Initialize the exception with polygon category validation context.

        Args:
            reason: Specific reason for invalid categories (e.g., "none_category_list",
                "none_category").
        """
        self._check_valid_reason(reason)
        self.reason = reason

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_category_list",
            "none_category",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid polygon categories found. "
        if self.reason == "none_category_list":
            msg += (
                "Found at least one list of polygon categories with None value. Must send a "
                "list of categories, one category per polygon."
            )
        elif self.reason == "none_category":
            msg += (
                "Found at least one category label with None value. Each polygon category "
                "must be string. Empty strings are allowed"
            )
        return msg


class InvalidPolygonScores(ValidationError, Exception):
    """Raised when polygon confidence scores are invalid or out of bounds."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Polygon_Scores"

    def __init__(self, reason: str) -> None:
        """Initialize the exception with polygon score validation context.

        Args:
            reason: Specific reason for invalid scores (e.g., "none_score_list",
                "scores_out_of_bounds").
        """
        self._check_valid_reason(reason)
        self.reason = reason

    @staticmethod
    def _check_valid_reason(reason: str) -> None:
        possible_reasons = (
            "none_score_list",
            "scores_out_of_bounds",
        )
        if reason not in possible_reasons:
            raise ValueError(
                f"Invalid reason {reason}. Possible reasons are: "
                f"{', '.join(possible_reasons)}."
            )

    def error_message(self) -> str:
        """Return the error message for this exception."""
        msg = "Invalid polygon scores found. "
        if self.reason == "none_score_list":
            msg += (
                "Found at least one list of polygon scores with None value. This field is "
                "optional. If sent, you must send a confidence score per polygon"
            )
        elif self.reason == "scores_out_of_bounds":
            msg += (
                "Found at least one confidence score out of bounds. "
                "Confidence scores must be between 0 and 1"
            )
        return msg


class InvalidNumClassesMultiClassMap(ValidationError):
    """Raised when multi-class dictionary contains invalid number of classes."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Num_classes_Multi_Class_Map"

    def __init__(
        self, dict_col_to_list_of_invalid_num_classes: dict[str, list[str]]
    ) -> None:
        """Initialize the exception with multi-class number validation context.

        Args:
            dict_col_to_list_of_invalid_num_classes: Mapping of columns to lists of
                invalid number of classes found.
        """
        self.invalid_col_num_classes = dict_col_to_list_of_invalid_num_classes

    def error_message(self) -> str:
        """Return the error message for this exception."""
        err_msg = ""
        for (
            col,
            list_invalid_num_classes,
        ) in self.invalid_col_num_classes.items():
            num_invalid_num_classes = len(list_invalid_num_classes)
            set_invalid_num_classes = set(
                list_invalid_num_classes
            )  # to de-duplicate
            err_msg += (
                f"Multi-Class dictionary for the following column: {col} had {num_invalid_num_classes} rows "
                f"containing an invalid number of classes. The dictionary must contain at least 1 class "
                f"and at most {MAX_NUMBER_OF_MULTI_CLASS_CLASSES} classes. Found rows with the following "
                f"invalid number of classes: {log_a_list(list(set_invalid_num_classes), 'and')}\n"
            )
        return err_msg


class InvalidMultiClassClassNameLength(ValidationError):
    """Raised when multi-class class names exceed maximum length."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Multi_Class_Class_Name_Length"

    def __init__(self, invalid_col_class_name: dict[str, set]) -> None:
        """Initialize the exception with multi-class name length validation context.

        Args:
            invalid_col_class_name: Mapping of columns to sets of invalid class names.
        """
        self.invalid_col_class_name = invalid_col_class_name

    def error_message(self) -> str:
        """Return the error message for this exception."""
        err_msg = ""
        for col, class_names in self.invalid_col_class_name.items():
            # limit to 10
            class_names = (
                list(class_names)[:10]
                if len(class_names) > 10
                else list(class_names)
            )
            err_msg += (
                f"Found some invalid class names: {log_a_list(class_names, 'and')} "
                f"in the {col} column. Class names must have at least one character "
                f"and less than {MAX_MULTI_CLASS_NAME_LENGTH}.\n"
            )
        return err_msg


class InvalidMultiClassPredScoreValue(ValidationError):
    """Raised when multi-class prediction scores are outside valid range."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Multi_Class_Pred_Score_Value"

    def __init__(self, invalid_col_class_scores: dict[str, set]) -> None:
        """Initialize the exception with multi-class prediction score validation context.

        Args:
            invalid_col_class_scores: Mapping of columns to sets of invalid scores.
        """
        self.invalid_col_class_scores = invalid_col_class_scores

    def error_message(self) -> str:
        """Return the error message for this exception."""
        err_msg = ""
        for col, scores in self.invalid_col_class_scores.items():
            # limit to 10
            scores = list(scores)[:10] if len(scores) > 10 else list(scores)
            err_msg += (
                f"Found some invalid scores: {log_a_list(scores, 'and')} in the {col} column that was "
                "invalid. All scores (values in dictionary) must be between 0 and 1, inclusive. \n"
            )
        return err_msg


class InvalidMultiClassActScoreValue(ValidationError):
    """Raised when multi-class actual scores are not 0 or 1."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Multi_Class_Act_Score_Value"

    def __init__(self, name: str) -> None:
        """Initialize the exception with multi-class actual score validation context.

        Args:
            name: Name of the column with invalid actual scores.
        """
        self.name = name

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Found at least one score in the '{self.name}' column that was invalid. "
            f"All scores (values) must be either 0 or 1."
        )


class InvalidMultiClassThresholdClasses(ValidationError):
    """Raised when prediction and threshold score dictionaries have mismatched classes."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Multi_Class_Threshold_Classes"

    def __init__(
        self, name: str, prediction_class_set: set, threshold_class_set: set
    ) -> None:
        """Initialize the exception with multi-class threshold validation context.

        Args:
            name: Name of the field being validated.
            prediction_class_set: Set of classes in prediction scores dictionary.
            threshold_class_set: Set of classes in threshold scores dictionary.
        """
        self.name = name
        self.prediction_class_set = prediction_class_set
        self.threshold_class_set = threshold_class_set

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Multi-Class Prediction Scores and Threshold Scores Dictionaries must contain the same "
            f"classes. The following classes of the Prediction Scores Dictionary are not in the Threshold "
            f"Scores Dictionary: {self.prediction_class_set.difference(self.threshold_class_set)}"
            "\nThe following classes of the Threshold Scores Dictionary are not in the Prediction Scores "
            f"Dictionary: {self.threshold_class_set.difference(self.prediction_class_set)}\n"
        )


class InvalidAdditionalHeaders(ValidationError):
    """Raised when additional headers use reserved header names."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Additional_Headers"

    def __init__(self, invalid_headers: Iterable) -> None:
        """Initialize the exception with invalid headers context.

        Args:
            invalid_headers: Headers that use reserved names.
        """
        self.invalid_header_names = invalid_headers

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            "Found invalid additional header, cannot use reserved headers named: "
            f"{', '.join(map(str, self.invalid_header_names))}."
        )


class InvalidRecord(ValidationError):
    """Raised when records contain invalid or all-null column sets."""

    def __repr__(self) -> str:
        """Return a string representation for debugging and logging."""
        return "Invalid_Record"

    def __init__(self, columns: list[str], indexes: list[int]) -> None:
        """Initialize the exception with invalid record context.

        Args:
            columns: Columns that form an invalid all-null set.
            indexes: Row indexes containing the invalid records.
        """
        self.columns = columns
        self.indexes = indexes

    def error_message(self) -> str:
        """Return the error message for this exception."""
        return (
            f"Invalid column set full of null values in one or more rows.\n"
            f"\nProblematic Column Set:\n{log_a_list(self.columns, 'and')}\n"
            f"\nProblematic Rows:\n{log_a_list(self.indexes, join_word='and')}\n"
            "\nThis violates one of the following requirements:\n"
            " - If training environment: Prediction or actual columns cannot be all null.\n"
            " - If production environment: Prediction and actual columns cannot be all null.\n"
            " - If you are sending SHAP values, make sure not all your SHAP values are null "
            "in any given row.\n"
        )
