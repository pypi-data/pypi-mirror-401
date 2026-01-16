# CDKTF prebuilt bindings for hashicorp/kubernetes provider version 2.38.0

This repo builds and publishes the [Terraform kubernetes provider](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktn/provider-kubernetes](https://www.npmjs.com/package/@cdktn/provider-kubernetes).

`npm install @cdktn/provider-kubernetes`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktn-provider-kubernetes](https://pypi.org/project/cdktn-provider-kubernetes).

`pipenv install cdktn-provider-kubernetes`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/Io.Cdktn.Cdktn.Providers.Kubernetes](https://www.nuget.org/packages/Io.Cdktn.Cdktn.Providers.Kubernetes).

`dotnet add package Io.Cdktn.Cdktn.Providers.Kubernetes`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.Io.Cdktn/cdktn-provider-kubernetes](https://mvnrepository.com/artifact/com.Io.Cdktn/cdktn-provider-kubernetes).

```
<dependency>
    <groupId>com.Io.Cdktn</groupId>
    <artifactId>cdktn-provider-kubernetes</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktn-io/cdktn-provider-kubernetes-go`](https://github.com/cdktn-io/cdktn-provider-kubernetes-go) package.

`go get github.com/cdktn-io/cdktn-provider-kubernetes-go/kubernetes/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktn-io/cdktn-provider-kubernetes-go/blob/main/kubernetes/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktn/provider-kubernetes).

## Versioning

This project is explicitly not tracking the Terraform kubernetes provider version 1:1. In fact, it always tracks `latest` of `~> 2.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf) - Last official release
* [Terraform kubernetes provider](https://registry.terraform.io/providers/hashicorp/kubernetes/2.38.0)
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
