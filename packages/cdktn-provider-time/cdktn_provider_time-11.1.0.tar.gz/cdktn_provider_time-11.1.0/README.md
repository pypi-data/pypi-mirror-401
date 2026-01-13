# CDKTF prebuilt bindings for hashicorp/time provider version 0.13.1

This repo builds and publishes the [Terraform time provider](https://registry.terraform.io/providers/hashicorp/time/0.13.1/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktn/provider-time](https://www.npmjs.com/package/@cdktn/provider-time).

`npm install @cdktn/provider-time`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktn-provider-time](https://pypi.org/project/cdktn-provider-time).

`pipenv install cdktn-provider-time`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/Io.Cdktn.Cdktn.Providers.Time](https://www.nuget.org/packages/Io.Cdktn.Cdktn.Providers.Time).

`dotnet add package Io.Cdktn.Cdktn.Providers.Time`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.Io.Cdktn/cdktn-provider-time](https://mvnrepository.com/artifact/com.Io.Cdktn/cdktn-provider-time).

```
<dependency>
    <groupId>com.Io.Cdktn</groupId>
    <artifactId>cdktn-provider-time</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktn-io/cdktn-provider-time-go`](https://github.com/cdktn-io/cdktn-provider-time-go) package.

`go get github.com/cdktn-io/cdktn-provider-time-go/time/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktn-io/cdktn-provider-time-go/blob/main/time/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktn/provider-time).

## Versioning

This project is explicitly not tracking the Terraform time provider version 1:1. In fact, it always tracks `latest` of `~> 0.7` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf) - Last official release
* [Terraform time provider](https://registry.terraform.io/providers/hashicorp/time/0.13.1)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://projen.io), which takes care of generating the entire repository.

### cdktn-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktn-io/cdktn-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTN Repository Manager](https://github.com/cdktn-io/cdktn-repository-manager/).
