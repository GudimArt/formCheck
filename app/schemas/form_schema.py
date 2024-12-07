from pydantic import BaseModel, model_validator, ConfigDict


class FormSchema(BaseModel):
    form_name: str
    model_config = ConfigDict(extra='allow')

    @model_validator(mode='before')
    def check_extra_fields(cls, values):
        extra_fields = {key: value for key, value in values.items() if key not in cls.model_fields}

        for field, value in extra_fields.items():
            if value not in ["email", "phone", "date", "text"]:
                raise ValueError(
                    f"Invalid field type for {field}: {value}. Expected one of 'email', 'phone', 'date', 'text'.")

        return values
