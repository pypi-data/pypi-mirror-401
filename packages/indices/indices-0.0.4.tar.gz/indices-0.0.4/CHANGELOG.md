# Changelog

## 0.0.4 (2026-01-10)

Full Changelog: [v0.0.3...v0.0.4](https://github.com/indicesio/indices-python/compare/v0.0.3...v0.0.4)

### Features

* **api:** add secrets APIs ([16f1cbe](https://github.com/indicesio/indices-python/commit/16f1cbeddd312eb10e1ae813ad40b3ad836dc4e2))
* **api:** add secrets APIs ([19f64f7](https://github.com/indicesio/indices-python/commit/19f64f7d9b9717ad2541c43b86496c39ecbd03cf))

## 0.0.3 (2026-01-10)

Full Changelog: [v0.0.2...v0.0.3](https://github.com/indicesio/indices-python/compare/v0.0.2...v0.0.3)

### Features

* **api:** improve examples ([b2aa0ed](https://github.com/indicesio/indices-python/commit/b2aa0ed184f512b82e245c39b399f32972f68c8f))
* **api:** manual updates ([b7364bb](https://github.com/indicesio/indices-python/commit/b7364bb2260e6fcdb0c7be226087a160320995e3))


### Bug Fixes

* ensure streams are always closed ([69d4b32](https://github.com/indicesio/indices-python/commit/69d4b327e19123f455fca874f2468e798880117c))
* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([57b79b0](https://github.com/indicesio/indices-python/commit/57b79b0bf617bee7bb445bd53aa34183325296ce))
* use async_to_httpx_files in patch method ([126eb61](https://github.com/indicesio/indices-python/commit/126eb613c202fdddf23808aacbdbdf675bcdccd2))


### Chores

* add missing docstrings ([8df9ee8](https://github.com/indicesio/indices-python/commit/8df9ee89d5143935931215e42602695ec1ea065c))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([e64b0a1](https://github.com/indicesio/indices-python/commit/e64b0a1fc2c5e067516938b2df54f1bda4523b0c))
* **docs:** use environment variables for authentication in code snippets ([9c03911](https://github.com/indicesio/indices-python/commit/9c0391185cfe2a091e2309dad60ce49dc447f394))
* **internal:** add `--fix` argument to lint script ([d783aed](https://github.com/indicesio/indices-python/commit/d783aedc00622a00a9ad0c93caed2c57db1e68ff))
* **internal:** add missing files argument to base client ([0493ee7](https://github.com/indicesio/indices-python/commit/0493ee7da82202ba3b442bef83b787d4a0137e38))
* **internal:** codegen related update ([b7f5b02](https://github.com/indicesio/indices-python/commit/b7f5b025e6443645688cebd3ecb9de0493e45f61))
* speedup initial import ([02a4942](https://github.com/indicesio/indices-python/commit/02a4942f1dea08583414c4d2a25507d6db3d406d))
* update lockfile ([12e35b4](https://github.com/indicesio/indices-python/commit/12e35b4b0170fb54100b1c1d98006317592b3fb3))

## 0.0.2 (2025-11-27)

Full Changelog: [v0.0.1...v0.0.2](https://github.com/indicesio/indices-python/compare/v0.0.1...v0.0.2)

### Features

* **api:** config updates ([88eadb3](https://github.com/indicesio/indices-python/commit/88eadb3d17bb0ada31c4fcd6fed1838d47916e81))
* **api:** update openapi spec (v1beta, etc) ([546f449](https://github.com/indicesio/indices-python/commit/546f44918e9b02c6cda3abcab760f2d954e955ec))


### Bug Fixes

* **client:** close streams without requiring full consumption ([959e13b](https://github.com/indicesio/indices-python/commit/959e13b69b92580d77aaa31f33adc3abccb50589))
* compat with Python 3.14 ([a37a195](https://github.com/indicesio/indices-python/commit/a37a1954165cc58e4b2f48cf8fb071455b191900))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([b4d1653](https://github.com/indicesio/indices-python/commit/b4d165320434b8447770e0cb417be404d21e0559))


### Chores

* add Python 3.14 classifier and testing ([541071b](https://github.com/indicesio/indices-python/commit/541071bf220a04ad50593691d34f2d3a96848f5f))
* **internal/tests:** avoid race condition with implicit client cleanup ([844f1fb](https://github.com/indicesio/indices-python/commit/844f1fb36c363c4e60d05bd311ed96115db3244c))
* **internal:** grammar fix (it's -&gt; its) ([49e8427](https://github.com/indicesio/indices-python/commit/49e8427b5299817d6bc5a06cec3deed1f164cbc0))
* **package:** drop Python 3.8 support ([daf5eee](https://github.com/indicesio/indices-python/commit/daf5eee6e9478719c680e775530b436b90870a84))

## 0.0.1 (2025-10-20)

Full Changelog: [v0.0.1...v0.0.1](https://github.com/indicesio/indices-python/compare/v0.0.1...v0.0.1)

### Features

* **api:** manual updates ([bd1ba01](https://github.com/indicesio/indices-python/commit/bd1ba01702edb85b98309a8f4b8b626c7a4f34f1))


### Chores

* update SDK settings ([29395f4](https://github.com/indicesio/indices-python/commit/29395f42da941577e78d2e18f310dfdfac11e044))
* update SDK settings ([7e79028](https://github.com/indicesio/indices-python/commit/7e79028fed7be3b520ff233352d28d0b9518d2ab))
