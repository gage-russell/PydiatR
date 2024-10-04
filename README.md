[![python-package](https://github.com/gage-russell/PydiatR/actions/workflows/python-package.yaml/badge.svg)](https://github.com/gage-russell/PydiatR/actions/workflows/python-package.yaml)
[![python-publish](https://github.com/gage-russell/PydiatR/actions/workflows/python-publish.yaml/badge.svg)](https://github.com/gage-russell/PydiatR/actions/workflows/python-publish.yaml)
[![pypi](https://img.shields.io/pypi/v/pydiatr)](https://pypi.org/project/pydiatr/)
[![license](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://raw.githubusercontent.com/gage-russell/pydiatr/main/LICENSE)
# PydiatR
The python MediatR.

## Example Usage
```python
from pydiatr.handler import AbstractHandler, AbstractRequest, AbstractResponse
from pydiatr.registry import Registry

registry = Registry()

class CreateUserRequest(AbstractRequest):
    username: str
    email: str

class CreateUserResponse(AbstractResponse):
    success: bool

@registry.decorate_handler
class CreateUserHandler(AbstractHandler[CreateUserRequest, CreateUserResponse]):

    async def handle(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"Creating user: {request.username} with email: {request.email}")
        return CreateUserResponse(success=True)

response = await registry.dispatch(CreateUserRequest)
```
# TODO:
* Abstract/DRY CI/CD
* Auto version bumping in CI/CD based on commit message using `poetry version <option>`
* Tests
* Test coverage and coverage comment on PR
* Coverage badge
* README
* FastAPI example
* FastAPI cookiecutter?
* Add post-commit hooks / checks that pre-commit hooks are being used
