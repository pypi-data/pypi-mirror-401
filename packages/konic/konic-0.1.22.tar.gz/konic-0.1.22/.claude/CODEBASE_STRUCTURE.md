.
└── src
    └── konic
        ├── __init__.py
        ├── agent
        │   ├── __init__.py
        │   ├── agent.py
        │   └── base.py
        ├── callback
        │   ├── __init__.py
        │   ├── base.py
        │   ├── callback.py
        │   ├── decorators.py
        │   ├── enums.py
        │   └── utils.py
        ├── cli
        │   ├── __init__.py
        │   ├── boilerplates
        │   │   ├── basic
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   ├── callback
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   ├── csv_streamer
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   ├── custom
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   ├── finetuning_advanced
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   ├── finetuning_basic
        │   │   │   └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │   │       └── agent.py
        │   │   └── full
        │   │       └── {{cookiecutter.name.replace(" ", "-").lower()}}
        │   │           └── agent.py
        │   ├── client
        │   │   ├── __init__.py
        │   │   └── api_client.py
        │   ├── decorators.py
        │   ├── enums.py
        │   ├── env_keys.py
        │   ├── root.py
        │   ├── src
        │   │   ├── __init__.py
        │   │   ├── agents.py
        │   │   ├── artifacts.py
        │   │   ├── data.py
        │   │   ├── health.py
        │   │   ├── inference.py
        │   │   ├── models.py
        │   │   └── training.py
        │   └── utils.py
        ├── common
        │   ├── __init__.py
        │   └── errors
        │       ├── __init__.py
        │       ├── base.py
        │       └── cli.py
        ├── engine
        │   ├── __init__.py
        │   ├── train.py
        │   └── utils.py
        ├── environment
        │   ├── __init__.py
        │   ├── base.py
        │   ├── core.py
        │   ├── environments.py
        │   ├── reward
        │   │   ├── __init__.py
        │   │   ├── base.py
        │   │   ├── decorators.py
        │   │   ├── enums.py
        │   │   ├── reducers
        │   │   │   ├── __init__.py
        │   │   │   ├── base.py
        │   │   │   └── strategy.py
        │   │   ├── reward.py
        │   │   └── utils.py
        │   ├── space
        │   │   ├── __init__.py
        │   │   ├── base.py
        │   │   ├── categorical
        │   │   │   ├── base.py
        │   │   │   └── strategy.py
        │   │   ├── space.py
        │   │   └── type
        │   │       ├── __init__.py
        │   │       └── base.py
        │   ├── termination
        │   │   ├── __init__.py
        │   │   ├── base.py
        │   │   ├── decorators.py
        │   │   ├── enums.py
        │   │   ├── reducers
        │   │   │   ├── __init__.py
        │   │   │   ├── base.py
        │   │   │   └── strategy.py
        │   │   ├── termination.py
        │   │   └── utils.py
        │   └── type
        │       ├── __init__.py
        │       └── base.py
        ├── finetuning
        │   ├── __init__.py
        │   ├── agent.py
        │   ├── backends
        │   │   ├── __init__.py
        │   │   ├── base.py
        │   │   ├── capabilities.py
        │   │   ├── native
        │   │   │   ├── __init__.py
        │   │   │   ├── advantage.py
        │   │   │   ├── backend.py
        │   │   │   └── ppo.py
        │   │   ├── result.py
        │   │   ├── shared
        │   │   │   ├── __init__.py
        │   │   │   ├── generation.py
        │   │   │   ├── mixins.py
        │   │   │   └── rewards.py
        │   │   └── trl
        │   │       ├── __init__.py
        │   │       ├── adapter
        │   │       │   ├── __init__.py
        │   │       │   ├── callback.py
        │   │       │   ├── config.py
        │   │       │   └── reward.py
        │   │       ├── base.py
        │   │       ├── dpo.py
        │   │       └── grpo.py
        │   ├── callback.py
        │   ├── config.py
        │   ├── dataset.py
        │   ├── engine.py
        │   ├── environment.py
        │   ├── module.py
        │   └── reward.py
        ├── module
        │   ├── __init__.py
        │   ├── base.py
        │   ├── ppo.py
        │   └── type.py
        └── runtime
            ├── __init__.py
            ├── agent.py
            └── data.py

43 directories, 107 files
