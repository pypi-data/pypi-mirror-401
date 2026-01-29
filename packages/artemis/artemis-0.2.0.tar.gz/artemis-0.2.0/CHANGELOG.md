# Changelog

## 0.2.0 (2026-01-15)

Full Changelog: [v0.1.2...v0.2.0](https://github.com/Artemis-xyz/artemis/compare/v0.1.2...v0.2.0)

### Features

* **api:** api update ([e2971e2](https://github.com/Artemis-xyz/artemis/commit/e2971e2f1328ee6c68c8bef85b09ee919219b0e5))
* **api:** api update ([e1bf8c3](https://github.com/Artemis-xyz/artemis/commit/e1bf8c364e4cf1608878512ad34ea16d2b9c1c20))
* **api:** api update ([f92b3e2](https://github.com/Artemis-xyz/artemis/commit/f92b3e2298356876d576dc8f5585cc694e59ad86))
* **api:** api update ([bb3d6a7](https://github.com/Artemis-xyz/artemis/commit/bb3d6a79729bfaabcbea1cbd01a26d1cf7ab90a5))
* **api:** api update ([38b6e58](https://github.com/Artemis-xyz/artemis/commit/38b6e585579abd3690f55049e59f355ade8ae264))
* **api:** api update ([43f2f6f](https://github.com/Artemis-xyz/artemis/commit/43f2f6ff2fe15a0db84f7dc68cf88b06e7cc3aa6))
* **api:** api update ([b1d236d](https://github.com/Artemis-xyz/artemis/commit/b1d236d774b4a62c031044f496ad01e80522a374))
* **api:** api update ([166c9a3](https://github.com/Artemis-xyz/artemis/commit/166c9a3e568bbb08445d87ee453a443b8d605519))
* **api:** api update ([ddaf54b](https://github.com/Artemis-xyz/artemis/commit/ddaf54b8f5fc502b2fcf1da5f470743ef6d75c9e))
* **api:** api update ([77a3ea9](https://github.com/Artemis-xyz/artemis/commit/77a3ea918b18f460070222db964966de3e8809f5))
* **api:** api update ([3281776](https://github.com/Artemis-xyz/artemis/commit/32817769a19625b361f72df109fcd5512084bea1))
* **api:** api update ([2697fab](https://github.com/Artemis-xyz/artemis/commit/2697fab4a42846e74b07ae194d6163d123fc1a01))
* **api:** api update ([a6cea69](https://github.com/Artemis-xyz/artemis/commit/a6cea69ca90f253cfbd4f6a85cd4049a436c4023))
* **api:** api update ([f0a5704](https://github.com/Artemis-xyz/artemis/commit/f0a5704fc6d3a1da5e16cc6d346de31ad80f0c97))
* **api:** manual updates ([e750d76](https://github.com/Artemis-xyz/artemis/commit/e750d7644112229367b4752c3457e61939dc285c))
* **client:** add support for binary request streaming ([5eff653](https://github.com/Artemis-xyz/artemis/commit/5eff6535668a5ebd6721b997029afb467763dce2))


### Bug Fixes

* **client:** close streams without requiring full consumption ([66c4b6b](https://github.com/Artemis-xyz/artemis/commit/66c4b6b5b0c6c640dcc74d0a9a73d1cb2aafd03d))
* compat with Python 3.14 ([a56027c](https://github.com/Artemis-xyz/artemis/commit/a56027ca5557e26bf3d75023f26589d5492bca9a))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([2a0af95](https://github.com/Artemis-xyz/artemis/commit/2a0af95ff91fcdecc47b963f23d396cfb2768df8))
* **types:** allow pyright to infer TypedDict types within SequenceNotStr ([f6a17c2](https://github.com/Artemis-xyz/artemis/commit/f6a17c2cc6d6454251f9477eb6dec0f4b20038c0))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([f2b9ae8](https://github.com/Artemis-xyz/artemis/commit/f2b9ae844fa295735bdb77976f7333f5bb5c2aa4))
* **deps:** mypy 1.18.1 has a regression, pin to 1.17 ([317d259](https://github.com/Artemis-xyz/artemis/commit/317d2596d9a1a14803add610fe8f68c8726414ee))
* do not install brew dependencies in ./scripts/bootstrap by default ([17b1b4d](https://github.com/Artemis-xyz/artemis/commit/17b1b4df68ad74a2a015d9d025064c519dbca92e))
* **internal/tests:** avoid race condition with implicit client cleanup ([cd6c682](https://github.com/Artemis-xyz/artemis/commit/cd6c682d5b37726e353831ded65ec4d4b10a583c))
* **internal:** add missing files argument to base client ([8455a9a](https://github.com/Artemis-xyz/artemis/commit/8455a9ad79580c41db8259e49954a8cdb6cabe4f))
* **internal:** detect missing future annotations with ruff ([8097a11](https://github.com/Artemis-xyz/artemis/commit/8097a118707ca06b1698b0027623fcd809f0202d))
* **internal:** grammar fix (it's -&gt; its) ([d24056c](https://github.com/Artemis-xyz/artemis/commit/d24056c16b8bfcc620b342d65d3437d1c4fb62ce))
* **internal:** update pydantic dependency ([4a338c7](https://github.com/Artemis-xyz/artemis/commit/4a338c7379b5367fcbc928e3eab1c2c533c40279))
* **package:** drop Python 3.8 support ([759a16e](https://github.com/Artemis-xyz/artemis/commit/759a16e8992560c8b8a3a6f8c234fc7779d37a22))
* **types:** change optional parameter type from NotGiven to Omit ([51bcc68](https://github.com/Artemis-xyz/artemis/commit/51bcc6800e1463da02ce6e9d95cdc54f27035479))

## 0.1.2 (2025-09-15)

Full Changelog: [v0.1.1...v0.1.2](https://github.com/Artemis-xyz/artemis/compare/v0.1.1...v0.1.2)

### Features

* **api:** api update ([4d098b0](https://github.com/Artemis-xyz/artemis/commit/4d098b0f9198f987abcc8a4bc74bd9219929e6a8))
* **api:** api update ([3bf6ade](https://github.com/Artemis-xyz/artemis/commit/3bf6aded6351cc55f201ea2110943455bd84382e))
* **api:** api update ([7b37955](https://github.com/Artemis-xyz/artemis/commit/7b3795597ce19693aab02849a69ca1d6b48a70d7))
* **api:** api update ([1f54e4a](https://github.com/Artemis-xyz/artemis/commit/1f54e4a2ab9f5cf2244a5159d1808a8c1e581616))
* **api:** api update ([b60906c](https://github.com/Artemis-xyz/artemis/commit/b60906c7eb024fce36086be8e9df0b1ec53b12bb))
* **api:** api update ([c454e05](https://github.com/Artemis-xyz/artemis/commit/c454e05bbd017c4eb6cd8ca65aede789b30a519c))
* **api:** api update ([fb8a6d9](https://github.com/Artemis-xyz/artemis/commit/fb8a6d957debcfce3fbdd81e07781153c5a71fe8))
* **api:** api update ([67c8d7c](https://github.com/Artemis-xyz/artemis/commit/67c8d7ce264bd1d67ac320ce7094e9940abc99b0))
* clean up environment call outs ([4e929bd](https://github.com/Artemis-xyz/artemis/commit/4e929bdd13f4c6ed0fa6a01adfdec8863a9a6d7d))
* **client:** add support for aiohttp ([6e4dbb0](https://github.com/Artemis-xyz/artemis/commit/6e4dbb0f747cb5a9783378780715f3315684a967))
* **client:** support file upload requests ([9125779](https://github.com/Artemis-xyz/artemis/commit/9125779560245b9824e885763d865fd73819bb92))
* improve future compat with pydantic v3 ([e2f2d8d](https://github.com/Artemis-xyz/artemis/commit/e2f2d8de974bff056dded5854adea7aa910b9498))


### Bug Fixes

* **ci:** correct conditional ([02b3eb7](https://github.com/Artemis-xyz/artemis/commit/02b3eb75acba1078bcdf956f31c574da292dbf2e))
* **ci:** release-doctor — report correct token name ([34cc6b6](https://github.com/Artemis-xyz/artemis/commit/34cc6b6e070dd6ad756ed7ea1eb48e8d9e561f54))
* **client:** correctly parse binary response | stream ([6c07bbd](https://github.com/Artemis-xyz/artemis/commit/6c07bbd67fae630f1991ea60a85c94de55da0b47))
* **client:** don't send Content-Type header on GET requests ([bb7bd7f](https://github.com/Artemis-xyz/artemis/commit/bb7bd7f9d34f91e1a220d8d3a52e50f5ed868efe))
* **parsing:** correctly handle nested discriminated unions ([11c993c](https://github.com/Artemis-xyz/artemis/commit/11c993c3900a845ea061d8144c9715532045d89d))
* **parsing:** ignore empty metadata ([bfcefd4](https://github.com/Artemis-xyz/artemis/commit/bfcefd442306977a3d08c986e6b98af5da1f13a0))
* **parsing:** parse extra field types ([7f07650](https://github.com/Artemis-xyz/artemis/commit/7f07650fe326da9ad29514aa2a4c134d0d1482e1))
* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([fde8c40](https://github.com/Artemis-xyz/artemis/commit/fde8c40a90d3bdaba485eede7c49b5e6d86762e1))


### Chores

* **ci:** change upload type ([8fae1b7](https://github.com/Artemis-xyz/artemis/commit/8fae1b7cf352dbbcf562c4e8f86359aa5d18630f))
* **ci:** enable for pull requests ([8d9fbe5](https://github.com/Artemis-xyz/artemis/commit/8d9fbe50ea97e921ac5d2e865dc1679e03a06d1e))
* **ci:** only run for pushes and fork pull requests ([33b6f17](https://github.com/Artemis-xyz/artemis/commit/33b6f17b15e03db8b3909daaaf60688b430df50b))
* **internal:** bump pinned h11 dep ([841ab9c](https://github.com/Artemis-xyz/artemis/commit/841ab9cc4bd82e110d2202065d106a007dd698e6))
* **internal:** codegen related update ([0eb477f](https://github.com/Artemis-xyz/artemis/commit/0eb477f17011c1b68b4430484bbb7e433cac6b32))
* **internal:** fix ruff target version ([2354773](https://github.com/Artemis-xyz/artemis/commit/2354773329eeed453e7e80c36599ee3c62f43287))
* **internal:** update comment in script ([ee5d49d](https://github.com/Artemis-xyz/artemis/commit/ee5d49d3aa6fae98b854247e378f7ef73bcc1249))
* **internal:** update conftest.py ([31cbef6](https://github.com/Artemis-xyz/artemis/commit/31cbef6e0d5d20d85af9924304f2526f3d721122))
* **package:** mark python 3.13 as supported ([769efbe](https://github.com/Artemis-xyz/artemis/commit/769efbee72d7b795b699cb21692c425200ae0bf5))
* **project:** add settings file for vscode ([18695a6](https://github.com/Artemis-xyz/artemis/commit/18695a61fb1699cb8e839a5887b193210e7b5b5b))
* **readme:** fix version rendering on pypi ([779eb9d](https://github.com/Artemis-xyz/artemis/commit/779eb9d2206ab971c42098a3868bdfede72b63fb))
* **readme:** update badges ([9a4b1be](https://github.com/Artemis-xyz/artemis/commit/9a4b1be58223f56008083558bc095ea845f54667))
* **tests:** add tests for httpx client instantiation & proxies ([4d3e4b9](https://github.com/Artemis-xyz/artemis/commit/4d3e4b9583a0f2ba7226aa440e1c5ef3c5fce87e))
* **tests:** run tests in parallel ([55d1060](https://github.com/Artemis-xyz/artemis/commit/55d106014dcc2853ee68bb9fa877ea5b26e2d4dc))
* **tests:** simplify `get_platform` test ([3db0b17](https://github.com/Artemis-xyz/artemis/commit/3db0b17060efb355c4283a93cd31f361a97b12a6))
* **tests:** skip some failing tests on the latest python versions ([fbf6ebc](https://github.com/Artemis-xyz/artemis/commit/fbf6ebc9a350642d04eb2fa4f8bae39ac26abc4c))
* update @stainless-api/prism-cli to v5.15.0 ([8cf0230](https://github.com/Artemis-xyz/artemis/commit/8cf02309331cd6dcda96a0d40ce72d3dc4a847fb))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([1afa1dd](https://github.com/Artemis-xyz/artemis/commit/1afa1ddb416000a7b88bf29abc78817530b92899))

## 0.1.1 (2025-06-11)

Full Changelog: [v0.1.0...v0.1.1](https://github.com/Artemis-xyz/artemis/compare/v0.1.0...v0.1.1)

### Features

* **api:** api update ([75982a4](https://github.com/Artemis-xyz/artemis/commit/75982a4c1412d3e293c5c8bc61141100fe731482))
* **api:** api update ([8317c3f](https://github.com/Artemis-xyz/artemis/commit/8317c3f21898f02cdafcef2e905aef4c3bf66a1d))
* **api:** api update ([55a14f5](https://github.com/Artemis-xyz/artemis/commit/55a14f52828c9514aec55b3d97647f34d72db542))
* **api:** api update ([8ad5fcf](https://github.com/Artemis-xyz/artemis/commit/8ad5fcfa233d04812f188ec821dcf175af2af43a))


### Bug Fixes

* **package:** support direct resource imports ([ffe1237](https://github.com/Artemis-xyz/artemis/commit/ffe1237f5d9ea243072a3f7108410a067a3ff48f))


### Chores

* **ci:** fix installation instructions ([83263db](https://github.com/Artemis-xyz/artemis/commit/83263dbc2470ddd9011ccc6cab9a381182e02867))
* **ci:** upload sdks to package manager ([23b127f](https://github.com/Artemis-xyz/artemis/commit/23b127f890fb6c03b0f6556ce7a83b749a9052b3))
* **docs:** grammar improvements ([5f1fb2e](https://github.com/Artemis-xyz/artemis/commit/5f1fb2e18a3ac45b97b9bc6f44069dd13e63c18d))
* **docs:** remove reference to rye shell ([1b2a446](https://github.com/Artemis-xyz/artemis/commit/1b2a446a4b9144f7eb1fb6bc7af8b80286257c4a))
* **internal:** avoid errors for isinstance checks on proxies ([f4ad11a](https://github.com/Artemis-xyz/artemis/commit/f4ad11aa97fb51e4fb511b776eedfb1405c80384))
* **internal:** codegen related update ([48d04db](https://github.com/Artemis-xyz/artemis/commit/48d04db44cad4c39667aafdc7e1a5baf44d6ca54))
* **internal:** codegen related update ([ae42929](https://github.com/Artemis-xyz/artemis/commit/ae42929147ad79880694635e152b4255ad65d3c8))

## 0.1.0 (2025-05-07)

Full Changelog: [v0.0.1...v0.1.0](https://github.com/Artemis-xyz/artemis/compare/v0.0.1...v0.1.0)

### Features

* **api:** api update ([552e44a](https://github.com/Artemis-xyz/artemis/commit/552e44a0e4083fcfbba9f77fb4638704243a108a))
* **api:** api update ([f170cf6](https://github.com/Artemis-xyz/artemis/commit/f170cf6e001c7a70e06cc4b83af5311244bc4c26))
* **api:** api update ([#10](https://github.com/Artemis-xyz/artemis/issues/10)) ([b3302ce](https://github.com/Artemis-xyz/artemis/commit/b3302ce2f858014e2530e96c27d6be9b2bfede88))
* **client:** allow passing `NotGiven` for body ([#7](https://github.com/Artemis-xyz/artemis/issues/7)) ([9b87cc4](https://github.com/Artemis-xyz/artemis/commit/9b87cc4edaeafd3591dbfccba52b6a2f91f40f60))


### Bug Fixes

* **ci:** ensure pip is always available ([#20](https://github.com/Artemis-xyz/artemis/issues/20)) ([b06bd19](https://github.com/Artemis-xyz/artemis/commit/b06bd19791c64eac364765570bceacaa5705187c))
* **ci:** remove publishing patch ([#21](https://github.com/Artemis-xyz/artemis/issues/21)) ([86a370f](https://github.com/Artemis-xyz/artemis/commit/86a370fae92d86a4f3d4a5ce8ff9332285de6997))
* **client:** mark some request bodies as optional ([9b87cc4](https://github.com/Artemis-xyz/artemis/commit/9b87cc4edaeafd3591dbfccba52b6a2f91f40f60))
* **perf:** optimize some hot paths ([c68f63f](https://github.com/Artemis-xyz/artemis/commit/c68f63fbc5a649bbbdbe1718c2459c0162ccd690))
* **perf:** skip traversing types for NotGiven values ([9283aa4](https://github.com/Artemis-xyz/artemis/commit/9283aa4a013cdf8d118cce1f21799ba4b30a1530))
* **types:** handle more discriminated union shapes ([#19](https://github.com/Artemis-xyz/artemis/issues/19)) ([5bbda52](https://github.com/Artemis-xyz/artemis/commit/5bbda52b4f7275d1dc772da34aa86e248b0c5578))


### Chores

* **client:** minor internal fixes ([425301a](https://github.com/Artemis-xyz/artemis/commit/425301a86df604dd7c0253c5a7128396fad1a868))
* **docs:** update client docstring ([#13](https://github.com/Artemis-xyz/artemis/issues/13)) ([75a4929](https://github.com/Artemis-xyz/artemis/commit/75a4929d0925652e550f5d3d11bf1775f6fb9f80))
* fix typos ([#22](https://github.com/Artemis-xyz/artemis/issues/22)) ([b1e7c2d](https://github.com/Artemis-xyz/artemis/commit/b1e7c2df29588905c05d600ff09a2cba5e9f1d76))
* **internal:** base client updates ([4f43cc1](https://github.com/Artemis-xyz/artemis/commit/4f43cc173b3a14df2a3605738bcd007d5bd41885))
* **internal:** bump pyright version ([a4f15f2](https://github.com/Artemis-xyz/artemis/commit/a4f15f2b9eb5bee85f9d683dabac55cf956ab467))
* **internal:** bump rye to 0.44.0 ([#18](https://github.com/Artemis-xyz/artemis/issues/18)) ([e28b4f7](https://github.com/Artemis-xyz/artemis/commit/e28b4f764df3ce9229ab258903ee51e83ac32566))
* **internal:** codegen related update ([#17](https://github.com/Artemis-xyz/artemis/issues/17)) ([979b2e8](https://github.com/Artemis-xyz/artemis/commit/979b2e8262687e676103c5d09b7e81976047a825))
* **internal:** expand CI branch coverage ([5300422](https://github.com/Artemis-xyz/artemis/commit/53004222e98c194a924c9aefadd4a9da06ea56f3))
* **internal:** fix devcontainers setup ([#9](https://github.com/Artemis-xyz/artemis/issues/9)) ([60ecc64](https://github.com/Artemis-xyz/artemis/commit/60ecc6486b6589c7e54720a6c5be08f7f1d094e4))
* **internal:** properly set __pydantic_private__ ([#11](https://github.com/Artemis-xyz/artemis/issues/11)) ([e6b9478](https://github.com/Artemis-xyz/artemis/commit/e6b94784244428625ebc8de81f89f049b0aba0c1))
* **internal:** reduce CI branch coverage ([1997764](https://github.com/Artemis-xyz/artemis/commit/199776496a104512554039facd2ac657b65b574b))
* **internal:** remove extra empty newlines ([#16](https://github.com/Artemis-xyz/artemis/issues/16)) ([f104ff7](https://github.com/Artemis-xyz/artemis/commit/f104ff79edad01208fb5387f86456c574262250b))
* **internal:** remove trailing character ([#23](https://github.com/Artemis-xyz/artemis/issues/23)) ([443fbcb](https://github.com/Artemis-xyz/artemis/commit/443fbcb12d5ebde2e12b932991980a003860c095))
* **internal:** remove unused http client options forwarding ([#14](https://github.com/Artemis-xyz/artemis/issues/14)) ([4fdf048](https://github.com/Artemis-xyz/artemis/commit/4fdf048bee3392cbcf16bf504baba158caddf61e))
* **internal:** slight transform perf improvement ([#24](https://github.com/Artemis-xyz/artemis/issues/24)) ([971eaf2](https://github.com/Artemis-xyz/artemis/commit/971eaf2a506c9bf9e066d804b6ff9e590aa0578b))
* **internal:** update models test ([d1b4be5](https://github.com/Artemis-xyz/artemis/commit/d1b4be54b49f7cf1cc1c2e3c9b2faa030b9bb3a8))
* **internal:** update pyright settings ([d8f7cf3](https://github.com/Artemis-xyz/artemis/commit/d8f7cf35c7e3a4360eefb1f97cf829145add31a4))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#12](https://github.com/Artemis-xyz/artemis/issues/12)) ([0d123ef](https://github.com/Artemis-xyz/artemis/commit/0d123efb40635365e50847f4011c7efe6d10eb39))

## 0.0.1 (2025-02-20)

Full Changelog: [v0.0.1-alpha.0...v0.0.1](https://github.com/Artemis-xyz/artemis/compare/v0.0.1-alpha.0...v0.0.1)

### Chores

* go live ([#3](https://github.com/Artemis-xyz/artemis/issues/3)) ([cd2bb12](https://github.com/Artemis-xyz/artemis/commit/cd2bb129e07fd484bb1af650db44ad9dc1cc4a4a))
* sync repo ([018633f](https://github.com/Artemis-xyz/artemis/commit/018633f7495103403e8504e87204e189012719e1))
* update SDK settings ([#5](https://github.com/Artemis-xyz/artemis/issues/5)) ([e04c2ab](https://github.com/Artemis-xyz/artemis/commit/e04c2ab30fdeb63fd14824aebd67a2054957b430))
