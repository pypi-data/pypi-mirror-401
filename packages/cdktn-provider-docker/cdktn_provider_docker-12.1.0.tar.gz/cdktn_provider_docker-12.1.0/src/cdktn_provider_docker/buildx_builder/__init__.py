r'''
# `docker_buildx_builder`

Refer to the Terraform Registry for docs: [`docker_buildx_builder`](https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class BuildxBuilder(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilder",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder docker_buildx_builder}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bootstrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        buildkit_config: typing.Optional[builtins.str] = None,
        buildkit_flags: typing.Optional[builtins.str] = None,
        docker_container: typing.Optional[typing.Union["BuildxBuilderDockerContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes: typing.Optional[typing.Union["BuildxBuilderKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_attribute: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Sequence[builtins.str]] = None,
        remote: typing.Optional[typing.Union["BuildxBuilderRemote", typing.Dict[builtins.str, typing.Any]]] = None,
        use: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder docker_buildx_builder} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param append: Append a node to builder instead of changing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#append BuildxBuilder#append}
        :param bootstrap: Automatically boot the builder after creation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#bootstrap BuildxBuilder#bootstrap}
        :param buildkit_config: BuildKit daemon config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_config BuildxBuilder#buildkit_config}
        :param buildkit_flags: BuildKit flags to set for the builder. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_flags BuildxBuilder#buildkit_flags}
        :param docker_container: docker_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#docker_container BuildxBuilder#docker_container}
        :param driver: The driver to use for the Buildx builder (e.g., docker-container, kubernetes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver BuildxBuilder#driver}
        :param driver_options: Additional options for the Buildx driver in the form of ``key=value,...``. These options are driver-specific. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver_options BuildxBuilder#driver_options}
        :param endpoint: The endpoint or context to use for the Buildx builder, where context is the name of a context from docker context ls and endpoint is the address for Docker socket (eg. DOCKER_HOST value). By default, the current Docker configuration is used for determining the context/endpoint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#endpoint BuildxBuilder#endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#id BuildxBuilder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#kubernetes BuildxBuilder#kubernetes}
        :param name: The name of the Buildx builder. IF not specified, a random name will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#name BuildxBuilder#name}
        :param node_attribute: Create/modify node with given name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#node BuildxBuilder#node}
        :param platform: Fixed platforms for current node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#platform BuildxBuilder#platform}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#remote BuildxBuilder#remote}
        :param use: Set the current builder instance as the default for the current context. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#use BuildxBuilder#use}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e978ee7de1168113840100daaaff2a947d447d222d6e0e4ba5a5163072495d6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BuildxBuilderConfig(
            append=append,
            bootstrap=bootstrap,
            buildkit_config=buildkit_config,
            buildkit_flags=buildkit_flags,
            docker_container=docker_container,
            driver=driver,
            driver_options=driver_options,
            endpoint=endpoint,
            id=id,
            kubernetes=kubernetes,
            name=name,
            node_attribute=node_attribute,
            platform=platform,
            remote=remote,
            use=use,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a BuildxBuilder resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BuildxBuilder to import.
        :param import_from_id: The id of the existing BuildxBuilder that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BuildxBuilder to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96fbc7092fd63dd79e99304ec952e7339f71902fc424eb832a85834bb6821cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDockerContainer")
    def put_docker_container(
        self,
        *,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[builtins.str] = None,
        cpu_quota: typing.Optional[builtins.str] = None,
        cpuset_cpus: typing.Optional[builtins.str] = None,
        cpuset_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
        memory_swap: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        restart_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cgroup_parent: Sets the cgroup parent of the container if Docker is using the "cgroupfs" driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cgroup_parent BuildxBuilder#cgroup_parent}
        :param cpu_period: Sets the CPU CFS scheduler period for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_period BuildxBuilder#cpu_period}
        :param cpu_quota: Imposes a CPU CFS quota on the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_quota BuildxBuilder#cpu_quota}
        :param cpuset_cpus: Limits the set of CPU cores the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_cpus BuildxBuilder#cpuset_cpus}
        :param cpuset_mems: Limits the set of CPU memory nodes the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_mems BuildxBuilder#cpuset_mems}
        :param cpu_shares: Configures CPU shares (relative weight) of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_shares BuildxBuilder#cpu_shares}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param env: Sets environment variables in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#env BuildxBuilder#env}
        :param image: Sets the BuildKit image to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param memory: Sets the amount of memory the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        :param memory_swap: Sets the memory swap limit for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory_swap BuildxBuilder#memory_swap}
        :param network: Sets the network mode for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#network BuildxBuilder#network}
        :param restart_policy: Sets the container's restart policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#restart_policy BuildxBuilder#restart_policy}
        '''
        value = BuildxBuilderDockerContainer(
            cgroup_parent=cgroup_parent,
            cpu_period=cpu_period,
            cpu_quota=cpu_quota,
            cpuset_cpus=cpuset_cpus,
            cpuset_mems=cpuset_mems,
            cpu_shares=cpu_shares,
            default_load=default_load,
            env=env,
            image=image,
            memory=memory,
            memory_swap=memory_swap,
            network=network,
            restart_policy=restart_policy,
        )

        return typing.cast(None, jsii.invoke(self, "putDockerContainer", [value]))

    @jsii.member(jsii_name="putKubernetes")
    def put_kubernetes(
        self,
        *,
        annotations: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[builtins.str] = None,
        limits: typing.Optional[typing.Union["BuildxBuilderKubernetesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        loadbalance: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        nodeselector: typing.Optional[builtins.str] = None,
        qemu: typing.Optional[typing.Union["BuildxBuilderKubernetesQemu", typing.Dict[builtins.str, typing.Any]]] = None,
        replicas: typing.Optional[jsii.Number] = None,
        requests: typing.Optional[typing.Union["BuildxBuilderKubernetesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
        rootless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedulername: typing.Optional[builtins.str] = None,
        serviceaccount: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        tolerations: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Sets additional annotations on the deployments and pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#annotations BuildxBuilder#annotations}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param image: Sets the image to use for running BuildKit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param labels: Sets additional labels on the deployments and pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#labels BuildxBuilder#labels}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#limits BuildxBuilder#limits}
        :param loadbalance: Load-balancing strategy (sticky or random). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#loadbalance BuildxBuilder#loadbalance}
        :param namespace: Sets the Kubernetes namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#namespace BuildxBuilder#namespace}
        :param nodeselector: Sets the pod's nodeSelector label(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#nodeselector BuildxBuilder#nodeselector}
        :param qemu: qemu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#qemu BuildxBuilder#qemu}
        :param replicas: Sets the number of Pod replicas to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#replicas BuildxBuilder#replicas}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#requests BuildxBuilder#requests}
        :param rootless: Run the container as a non-root user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#rootless BuildxBuilder#rootless}
        :param schedulername: Sets the scheduler responsible for scheduling the pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#schedulername BuildxBuilder#schedulername}
        :param serviceaccount: Sets the pod's serviceAccountName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#serviceaccount BuildxBuilder#serviceaccount}
        :param timeout: Set the timeout limit for pod provisioning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#timeout BuildxBuilder#timeout}
        :param tolerations: Configures the pod's taint toleration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#tolerations BuildxBuilder#tolerations}
        '''
        value = BuildxBuilderKubernetes(
            annotations=annotations,
            default_load=default_load,
            image=image,
            labels=labels,
            limits=limits,
            loadbalance=loadbalance,
            namespace=namespace,
            nodeselector=nodeselector,
            qemu=qemu,
            replicas=replicas,
            requests=requests,
            rootless=rootless,
            schedulername=schedulername,
            serviceaccount=serviceaccount,
            timeout=timeout,
            tolerations=tolerations,
        )

        return typing.cast(None, jsii.invoke(self, "putKubernetes", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        cacert: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        servername: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cacert: Absolute path to the TLS certificate authority used for validation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cacert BuildxBuilder#cacert}
        :param cert: Absolute path to the TLS client certificate to present to buildkitd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cert BuildxBuilder#cert}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param key: Sets the TLS client key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#key BuildxBuilder#key}
        :param servername: TLS server name used in requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#servername BuildxBuilder#servername}
        '''
        value = BuildxBuilderRemote(
            cacert=cacert,
            cert=cert,
            default_load=default_load,
            key=key,
            servername=servername,
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAppend")
    def reset_append(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppend", []))

    @jsii.member(jsii_name="resetBootstrap")
    def reset_bootstrap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBootstrap", []))

    @jsii.member(jsii_name="resetBuildkitConfig")
    def reset_buildkit_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildkitConfig", []))

    @jsii.member(jsii_name="resetBuildkitFlags")
    def reset_buildkit_flags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildkitFlags", []))

    @jsii.member(jsii_name="resetDockerContainer")
    def reset_docker_container(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDockerContainer", []))

    @jsii.member(jsii_name="resetDriver")
    def reset_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriver", []))

    @jsii.member(jsii_name="resetDriverOptions")
    def reset_driver_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverOptions", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKubernetes")
    def reset_kubernetes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKubernetes", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNodeAttribute")
    def reset_node_attribute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeAttribute", []))

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @jsii.member(jsii_name="resetUse")
    def reset_use(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUse", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="dockerContainer")
    def docker_container(self) -> "BuildxBuilderDockerContainerOutputReference":
        return typing.cast("BuildxBuilderDockerContainerOutputReference", jsii.get(self, "dockerContainer"))

    @builtins.property
    @jsii.member(jsii_name="kubernetes")
    def kubernetes(self) -> "BuildxBuilderKubernetesOutputReference":
        return typing.cast("BuildxBuilderKubernetesOutputReference", jsii.get(self, "kubernetes"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(self) -> "BuildxBuilderRemoteOutputReference":
        return typing.cast("BuildxBuilderRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="appendInput")
    def append_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "appendInput"))

    @builtins.property
    @jsii.member(jsii_name="bootstrapInput")
    def bootstrap_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bootstrapInput"))

    @builtins.property
    @jsii.member(jsii_name="buildkitConfigInput")
    def buildkit_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildkitConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="buildkitFlagsInput")
    def buildkit_flags_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildkitFlagsInput"))

    @builtins.property
    @jsii.member(jsii_name="dockerContainerInput")
    def docker_container_input(self) -> typing.Optional["BuildxBuilderDockerContainer"]:
        return typing.cast(typing.Optional["BuildxBuilderDockerContainer"], jsii.get(self, "dockerContainerInput"))

    @builtins.property
    @jsii.member(jsii_name="driverInput")
    def driver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverInput"))

    @builtins.property
    @jsii.member(jsii_name="driverOptionsInput")
    def driver_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesInput")
    def kubernetes_input(self) -> typing.Optional["BuildxBuilderKubernetes"]:
        return typing.cast(typing.Optional["BuildxBuilderKubernetes"], jsii.get(self, "kubernetesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttributeInput")
    def node_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(self) -> typing.Optional["BuildxBuilderRemote"]:
        return typing.cast(typing.Optional["BuildxBuilderRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="useInput")
    def use_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useInput"))

    @builtins.property
    @jsii.member(jsii_name="append")
    def append(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "append"))

    @append.setter
    def append(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe50460855baebf4b73542e7b7f18776cfd505934e0c274a53b500f576f542c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "append", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bootstrap")
    def bootstrap(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bootstrap"))

    @bootstrap.setter
    def bootstrap(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d337a347946d3f01eefa8ce1fc90c4681d2054262cf8f46e7e6cc04a5c9754f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bootstrap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildkitConfig")
    def buildkit_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildkitConfig"))

    @buildkit_config.setter
    def buildkit_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d96356b227e5342fd922d3521e41a32cd96e7bc5018cb6024c3519e660641ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildkitConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="buildkitFlags")
    def buildkit_flags(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildkitFlags"))

    @buildkit_flags.setter
    def buildkit_flags(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efae3d395316e86aee85b289529041b1eaf57f9ddd2d5c518915ee9fc577c945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildkitFlags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driver")
    def driver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driver"))

    @driver.setter
    def driver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2fca5a0e7be0af9c8f77e2ee11a870d57f698d056e6dbaedf110fec6a2b740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driver", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOptions")
    def driver_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverOptions"))

    @driver_options.setter
    def driver_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e350f4f840bbac9f5d323d5a17b4edee95665a0d66b4c764bac7ecdbf6caca0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ab7b2c137f5aa251931206fb374a6bf870c3a12a5c53fd8abd50bc1e1bab36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3e420a7d6f04ebb97786186678e3435ff8cda41e94b0aefa23daf49489a7abc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c1471f95f73a87697704efe80b3cdb3e782649ac13f8454dc3728d571ebd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @node_attribute.setter
    def node_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4067cbe098e507978ce489692c9d240985994f83791d0984540debe7dd6401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75612131a54bed960843b3c7b9abee07f2564334a982c41a5725c4cc74f6e2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="use")
    def use(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "use"))

    @use.setter
    def use(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26531bf84b6598761a5a9760aa54b7a2feffbee1411e0f730a8a64344a8cfd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "use", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "append": "append",
        "bootstrap": "bootstrap",
        "buildkit_config": "buildkitConfig",
        "buildkit_flags": "buildkitFlags",
        "docker_container": "dockerContainer",
        "driver": "driver",
        "driver_options": "driverOptions",
        "endpoint": "endpoint",
        "id": "id",
        "kubernetes": "kubernetes",
        "name": "name",
        "node_attribute": "nodeAttribute",
        "platform": "platform",
        "remote": "remote",
        "use": "use",
    },
)
class BuildxBuilderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bootstrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        buildkit_config: typing.Optional[builtins.str] = None,
        buildkit_flags: typing.Optional[builtins.str] = None,
        docker_container: typing.Optional[typing.Union["BuildxBuilderDockerContainer", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        endpoint: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kubernetes: typing.Optional[typing.Union["BuildxBuilderKubernetes", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        node_attribute: typing.Optional[builtins.str] = None,
        platform: typing.Optional[typing.Sequence[builtins.str]] = None,
        remote: typing.Optional[typing.Union["BuildxBuilderRemote", typing.Dict[builtins.str, typing.Any]]] = None,
        use: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param append: Append a node to builder instead of changing it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#append BuildxBuilder#append}
        :param bootstrap: Automatically boot the builder after creation. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#bootstrap BuildxBuilder#bootstrap}
        :param buildkit_config: BuildKit daemon config file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_config BuildxBuilder#buildkit_config}
        :param buildkit_flags: BuildKit flags to set for the builder. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_flags BuildxBuilder#buildkit_flags}
        :param docker_container: docker_container block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#docker_container BuildxBuilder#docker_container}
        :param driver: The driver to use for the Buildx builder (e.g., docker-container, kubernetes). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver BuildxBuilder#driver}
        :param driver_options: Additional options for the Buildx driver in the form of ``key=value,...``. These options are driver-specific. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver_options BuildxBuilder#driver_options}
        :param endpoint: The endpoint or context to use for the Buildx builder, where context is the name of a context from docker context ls and endpoint is the address for Docker socket (eg. DOCKER_HOST value). By default, the current Docker configuration is used for determining the context/endpoint value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#endpoint BuildxBuilder#endpoint}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#id BuildxBuilder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kubernetes: kubernetes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#kubernetes BuildxBuilder#kubernetes}
        :param name: The name of the Buildx builder. IF not specified, a random name will be generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#name BuildxBuilder#name}
        :param node_attribute: Create/modify node with given name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#node BuildxBuilder#node}
        :param platform: Fixed platforms for current node. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#platform BuildxBuilder#platform}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#remote BuildxBuilder#remote}
        :param use: Set the current builder instance as the default for the current context. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#use BuildxBuilder#use}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(docker_container, dict):
            docker_container = BuildxBuilderDockerContainer(**docker_container)
        if isinstance(kubernetes, dict):
            kubernetes = BuildxBuilderKubernetes(**kubernetes)
        if isinstance(remote, dict):
            remote = BuildxBuilderRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552c4b130918a9743da4e84ba6082a1ce269edaffb52d4be17497a5125432afe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
            check_type(argname="argument bootstrap", value=bootstrap, expected_type=type_hints["bootstrap"])
            check_type(argname="argument buildkit_config", value=buildkit_config, expected_type=type_hints["buildkit_config"])
            check_type(argname="argument buildkit_flags", value=buildkit_flags, expected_type=type_hints["buildkit_flags"])
            check_type(argname="argument docker_container", value=docker_container, expected_type=type_hints["docker_container"])
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument driver_options", value=driver_options, expected_type=type_hints["driver_options"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kubernetes", value=kubernetes, expected_type=type_hints["kubernetes"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_attribute", value=node_attribute, expected_type=type_hints["node_attribute"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
            check_type(argname="argument use", value=use, expected_type=type_hints["use"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if append is not None:
            self._values["append"] = append
        if bootstrap is not None:
            self._values["bootstrap"] = bootstrap
        if buildkit_config is not None:
            self._values["buildkit_config"] = buildkit_config
        if buildkit_flags is not None:
            self._values["buildkit_flags"] = buildkit_flags
        if docker_container is not None:
            self._values["docker_container"] = docker_container
        if driver is not None:
            self._values["driver"] = driver
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if id is not None:
            self._values["id"] = id
        if kubernetes is not None:
            self._values["kubernetes"] = kubernetes
        if name is not None:
            self._values["name"] = name
        if node_attribute is not None:
            self._values["node_attribute"] = node_attribute
        if platform is not None:
            self._values["platform"] = platform
        if remote is not None:
            self._values["remote"] = remote
        if use is not None:
            self._values["use"] = use

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def append(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Append a node to builder instead of changing it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#append BuildxBuilder#append}
        '''
        result = self._values.get("append")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bootstrap(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically boot the builder after creation. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#bootstrap BuildxBuilder#bootstrap}
        '''
        result = self._values.get("bootstrap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def buildkit_config(self) -> typing.Optional[builtins.str]:
        '''BuildKit daemon config file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_config BuildxBuilder#buildkit_config}
        '''
        result = self._values.get("buildkit_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def buildkit_flags(self) -> typing.Optional[builtins.str]:
        '''BuildKit flags to set for the builder.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#buildkit_flags BuildxBuilder#buildkit_flags}
        '''
        result = self._values.get("buildkit_flags")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_container(self) -> typing.Optional["BuildxBuilderDockerContainer"]:
        '''docker_container block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#docker_container BuildxBuilder#docker_container}
        '''
        result = self._values.get("docker_container")
        return typing.cast(typing.Optional["BuildxBuilderDockerContainer"], result)

    @builtins.property
    def driver(self) -> typing.Optional[builtins.str]:
        '''The driver to use for the Buildx builder (e.g., docker-container, kubernetes).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver BuildxBuilder#driver}
        '''
        result = self._values.get("driver")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional options for the Buildx driver in the form of ``key=value,...``. These options are driver-specific.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#driver_options BuildxBuilder#driver_options}
        '''
        result = self._values.get("driver_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''The endpoint or context to use for the Buildx builder, where context is the name of a context from docker context ls and endpoint is the address for Docker socket (eg.

        DOCKER_HOST value). By default, the current Docker configuration is used for determining the context/endpoint value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#endpoint BuildxBuilder#endpoint}
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#id BuildxBuilder#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes(self) -> typing.Optional["BuildxBuilderKubernetes"]:
        '''kubernetes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#kubernetes BuildxBuilder#kubernetes}
        '''
        result = self._values.get("kubernetes")
        return typing.cast(typing.Optional["BuildxBuilderKubernetes"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Buildx builder. IF not specified, a random name will be generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#name BuildxBuilder#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_attribute(self) -> typing.Optional[builtins.str]:
        '''Create/modify node with given name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#node BuildxBuilder#node}
        '''
        result = self._values.get("node_attribute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fixed platforms for current node.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#platform BuildxBuilder#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def remote(self) -> typing.Optional["BuildxBuilderRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#remote BuildxBuilder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["BuildxBuilderRemote"], result)

    @builtins.property
    def use(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set the current builder instance as the default for the current context.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#use BuildxBuilder#use}
        '''
        result = self._values.get("use")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderDockerContainer",
    jsii_struct_bases=[],
    name_mapping={
        "cgroup_parent": "cgroupParent",
        "cpu_period": "cpuPeriod",
        "cpu_quota": "cpuQuota",
        "cpuset_cpus": "cpusetCpus",
        "cpuset_mems": "cpusetMems",
        "cpu_shares": "cpuShares",
        "default_load": "defaultLoad",
        "env": "env",
        "image": "image",
        "memory": "memory",
        "memory_swap": "memorySwap",
        "network": "network",
        "restart_policy": "restartPolicy",
    },
)
class BuildxBuilderDockerContainer:
    def __init__(
        self,
        *,
        cgroup_parent: typing.Optional[builtins.str] = None,
        cpu_period: typing.Optional[builtins.str] = None,
        cpu_quota: typing.Optional[builtins.str] = None,
        cpuset_cpus: typing.Optional[builtins.str] = None,
        cpuset_mems: typing.Optional[builtins.str] = None,
        cpu_shares: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
        memory_swap: typing.Optional[builtins.str] = None,
        network: typing.Optional[builtins.str] = None,
        restart_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cgroup_parent: Sets the cgroup parent of the container if Docker is using the "cgroupfs" driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cgroup_parent BuildxBuilder#cgroup_parent}
        :param cpu_period: Sets the CPU CFS scheduler period for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_period BuildxBuilder#cpu_period}
        :param cpu_quota: Imposes a CPU CFS quota on the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_quota BuildxBuilder#cpu_quota}
        :param cpuset_cpus: Limits the set of CPU cores the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_cpus BuildxBuilder#cpuset_cpus}
        :param cpuset_mems: Limits the set of CPU memory nodes the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_mems BuildxBuilder#cpuset_mems}
        :param cpu_shares: Configures CPU shares (relative weight) of the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_shares BuildxBuilder#cpu_shares}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param env: Sets environment variables in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#env BuildxBuilder#env}
        :param image: Sets the BuildKit image to use for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param memory: Sets the amount of memory the container can use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        :param memory_swap: Sets the memory swap limit for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory_swap BuildxBuilder#memory_swap}
        :param network: Sets the network mode for the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#network BuildxBuilder#network}
        :param restart_policy: Sets the container's restart policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#restart_policy BuildxBuilder#restart_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dbd7239a186057cb9ccfadf91f8c61a32c36702ef8a07f9b1cdc9506351344)
            check_type(argname="argument cgroup_parent", value=cgroup_parent, expected_type=type_hints["cgroup_parent"])
            check_type(argname="argument cpu_period", value=cpu_period, expected_type=type_hints["cpu_period"])
            check_type(argname="argument cpu_quota", value=cpu_quota, expected_type=type_hints["cpu_quota"])
            check_type(argname="argument cpuset_cpus", value=cpuset_cpus, expected_type=type_hints["cpuset_cpus"])
            check_type(argname="argument cpuset_mems", value=cpuset_mems, expected_type=type_hints["cpuset_mems"])
            check_type(argname="argument cpu_shares", value=cpu_shares, expected_type=type_hints["cpu_shares"])
            check_type(argname="argument default_load", value=default_load, expected_type=type_hints["default_load"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument memory_swap", value=memory_swap, expected_type=type_hints["memory_swap"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument restart_policy", value=restart_policy, expected_type=type_hints["restart_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cgroup_parent is not None:
            self._values["cgroup_parent"] = cgroup_parent
        if cpu_period is not None:
            self._values["cpu_period"] = cpu_period
        if cpu_quota is not None:
            self._values["cpu_quota"] = cpu_quota
        if cpuset_cpus is not None:
            self._values["cpuset_cpus"] = cpuset_cpus
        if cpuset_mems is not None:
            self._values["cpuset_mems"] = cpuset_mems
        if cpu_shares is not None:
            self._values["cpu_shares"] = cpu_shares
        if default_load is not None:
            self._values["default_load"] = default_load
        if env is not None:
            self._values["env"] = env
        if image is not None:
            self._values["image"] = image
        if memory is not None:
            self._values["memory"] = memory
        if memory_swap is not None:
            self._values["memory_swap"] = memory_swap
        if network is not None:
            self._values["network"] = network
        if restart_policy is not None:
            self._values["restart_policy"] = restart_policy

    @builtins.property
    def cgroup_parent(self) -> typing.Optional[builtins.str]:
        '''Sets the cgroup parent of the container if Docker is using the "cgroupfs" driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cgroup_parent BuildxBuilder#cgroup_parent}
        '''
        result = self._values.get("cgroup_parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_period(self) -> typing.Optional[builtins.str]:
        '''Sets the CPU CFS scheduler period for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_period BuildxBuilder#cpu_period}
        '''
        result = self._values.get("cpu_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_quota(self) -> typing.Optional[builtins.str]:
        '''Imposes a CPU CFS quota on the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_quota BuildxBuilder#cpu_quota}
        '''
        result = self._values.get("cpu_quota")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpuset_cpus(self) -> typing.Optional[builtins.str]:
        '''Limits the set of CPU cores the container can use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_cpus BuildxBuilder#cpuset_cpus}
        '''
        result = self._values.get("cpuset_cpus")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpuset_mems(self) -> typing.Optional[builtins.str]:
        '''Limits the set of CPU memory nodes the container can use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpuset_mems BuildxBuilder#cpuset_mems}
        '''
        result = self._values.get("cpuset_mems")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu_shares(self) -> typing.Optional[builtins.str]:
        '''Configures CPU shares (relative weight) of the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu_shares BuildxBuilder#cpu_shares}
        '''
        result = self._values.get("cpu_shares")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_load(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically load images to the Docker Engine image store. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        '''
        result = self._values.get("default_load")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets environment variables in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#env BuildxBuilder#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Sets the BuildKit image to use for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Sets the amount of memory the container can use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory_swap(self) -> typing.Optional[builtins.str]:
        '''Sets the memory swap limit for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory_swap BuildxBuilder#memory_swap}
        '''
        result = self._values.get("memory_swap")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''Sets the network mode for the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#network BuildxBuilder#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restart_policy(self) -> typing.Optional[builtins.str]:
        '''Sets the container's restart policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#restart_policy BuildxBuilder#restart_policy}
        '''
        result = self._values.get("restart_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderDockerContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildxBuilderDockerContainerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderDockerContainerOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2cb7e870463bca5c08f1b1d6cf57eb7971e59e1a067ff32d89b37ab1c12c691)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCgroupParent")
    def reset_cgroup_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCgroupParent", []))

    @jsii.member(jsii_name="resetCpuPeriod")
    def reset_cpu_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuPeriod", []))

    @jsii.member(jsii_name="resetCpuQuota")
    def reset_cpu_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuQuota", []))

    @jsii.member(jsii_name="resetCpusetCpus")
    def reset_cpuset_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpusetCpus", []))

    @jsii.member(jsii_name="resetCpusetMems")
    def reset_cpuset_mems(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpusetMems", []))

    @jsii.member(jsii_name="resetCpuShares")
    def reset_cpu_shares(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuShares", []))

    @jsii.member(jsii_name="resetDefaultLoad")
    def reset_default_load(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLoad", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetMemorySwap")
    def reset_memory_swap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemorySwap", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetRestartPolicy")
    def reset_restart_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestartPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="cgroupParentInput")
    def cgroup_parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cgroupParentInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuPeriodInput")
    def cpu_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuQuotaInput")
    def cpu_quota_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="cpusetCpusInput")
    def cpuset_cpus_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpusetCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="cpusetMemsInput")
    def cpuset_mems_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpusetMemsInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuSharesInput")
    def cpu_shares_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuSharesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLoadInput")
    def default_load_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultLoadInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="memorySwapInput")
    def memory_swap_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memorySwapInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="restartPolicyInput")
    def restart_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restartPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="cgroupParent")
    def cgroup_parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cgroupParent"))

    @cgroup_parent.setter
    def cgroup_parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33651599c3212198fd5334b5919f1f850851f00511461eaa00f00985355f5291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cgroupParent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuPeriod")
    def cpu_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuPeriod"))

    @cpu_period.setter
    def cpu_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5598b7e9e56a2d87fa58d5efe84f288b3f81de8671f0d69aa5aa737161070c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuQuota")
    def cpu_quota(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuQuota"))

    @cpu_quota.setter
    def cpu_quota(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b498cd2559bdac7810133f21df6f5733b0339380d8f59365479628d39654891c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpusetCpus")
    def cpuset_cpus(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpusetCpus"))

    @cpuset_cpus.setter
    def cpuset_cpus(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2f31ea5994040a7f03edc6f5cf335e335b00f4683c5314d1a5603f94f35962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpusetCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpusetMems")
    def cpuset_mems(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpusetMems"))

    @cpuset_mems.setter
    def cpuset_mems(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520ba5545304f041f47eefa2c9f670cb77a53496d9d0a8fc1722fea48f0a6390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpusetMems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cpuShares")
    def cpu_shares(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpuShares"))

    @cpu_shares.setter
    def cpu_shares(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d66ec8181dc1adcd88d966b335170487f0a7ad554f77d3dce7a7781629b2f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuShares", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLoad")
    def default_load(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultLoad"))

    @default_load.setter
    def default_load(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1555fd2d2bc7cbedfe21fac886eff84febe5dbd6aa72e86a020aa979ad06914e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLoad", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b475b4536ff0a91bfdf19c8b1635f3492c5a97fad63baca33b3ed3d9196170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6625f3e7a846df5c4a657c53a6e97a6f3e608f76980f42fcd622a28247dbaec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3642129eb3b452648de477ea348cbeda3f03fa43242e9480445215d7f935ef68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memorySwap")
    def memory_swap(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memorySwap"))

    @memory_swap.setter
    def memory_swap(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce20d79c2f1ba22efcc30b8ac0fa6039cb6f303faf0df667188ed1b0d53a3bd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memorySwap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aed8e3c9b73fae852ce48dc035134b2ad311b5d56a4d7e167882abfed6282c57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restartPolicy")
    def restart_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restartPolicy"))

    @restart_policy.setter
    def restart_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbf1acede18eb59c04722332dc330d5f6bf7272bb8fea8ce901b3d167f9777c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restartPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderDockerContainer]:
        return typing.cast(typing.Optional[BuildxBuilderDockerContainer], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BuildxBuilderDockerContainer],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3e386e51fc29cbdbcd61e9a5b6928ec4ced49ce56f261bba9477c2a07b9978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetes",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "default_load": "defaultLoad",
        "image": "image",
        "labels": "labels",
        "limits": "limits",
        "loadbalance": "loadbalance",
        "namespace": "namespace",
        "nodeselector": "nodeselector",
        "qemu": "qemu",
        "replicas": "replicas",
        "requests": "requests",
        "rootless": "rootless",
        "schedulername": "schedulername",
        "serviceaccount": "serviceaccount",
        "timeout": "timeout",
        "tolerations": "tolerations",
    },
)
class BuildxBuilderKubernetes:
    def __init__(
        self,
        *,
        annotations: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        image: typing.Optional[builtins.str] = None,
        labels: typing.Optional[builtins.str] = None,
        limits: typing.Optional[typing.Union["BuildxBuilderKubernetesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        loadbalance: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        nodeselector: typing.Optional[builtins.str] = None,
        qemu: typing.Optional[typing.Union["BuildxBuilderKubernetesQemu", typing.Dict[builtins.str, typing.Any]]] = None,
        replicas: typing.Optional[jsii.Number] = None,
        requests: typing.Optional[typing.Union["BuildxBuilderKubernetesRequests", typing.Dict[builtins.str, typing.Any]]] = None,
        rootless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        schedulername: typing.Optional[builtins.str] = None,
        serviceaccount: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        tolerations: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: Sets additional annotations on the deployments and pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#annotations BuildxBuilder#annotations}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param image: Sets the image to use for running BuildKit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param labels: Sets additional labels on the deployments and pods. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#labels BuildxBuilder#labels}
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#limits BuildxBuilder#limits}
        :param loadbalance: Load-balancing strategy (sticky or random). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#loadbalance BuildxBuilder#loadbalance}
        :param namespace: Sets the Kubernetes namespace. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#namespace BuildxBuilder#namespace}
        :param nodeselector: Sets the pod's nodeSelector label(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#nodeselector BuildxBuilder#nodeselector}
        :param qemu: qemu block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#qemu BuildxBuilder#qemu}
        :param replicas: Sets the number of Pod replicas to create. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#replicas BuildxBuilder#replicas}
        :param requests: requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#requests BuildxBuilder#requests}
        :param rootless: Run the container as a non-root user. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#rootless BuildxBuilder#rootless}
        :param schedulername: Sets the scheduler responsible for scheduling the pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#schedulername BuildxBuilder#schedulername}
        :param serviceaccount: Sets the pod's serviceAccountName. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#serviceaccount BuildxBuilder#serviceaccount}
        :param timeout: Set the timeout limit for pod provisioning. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#timeout BuildxBuilder#timeout}
        :param tolerations: Configures the pod's taint toleration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#tolerations BuildxBuilder#tolerations}
        '''
        if isinstance(limits, dict):
            limits = BuildxBuilderKubernetesLimits(**limits)
        if isinstance(qemu, dict):
            qemu = BuildxBuilderKubernetesQemu(**qemu)
        if isinstance(requests, dict):
            requests = BuildxBuilderKubernetesRequests(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f99aa3085ef502e08a7c188bb97a44ba8b8030869fcae887f44497bf49d297)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument default_load", value=default_load, expected_type=type_hints["default_load"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument loadbalance", value=loadbalance, expected_type=type_hints["loadbalance"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument nodeselector", value=nodeselector, expected_type=type_hints["nodeselector"])
            check_type(argname="argument qemu", value=qemu, expected_type=type_hints["qemu"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
            check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
            check_type(argname="argument rootless", value=rootless, expected_type=type_hints["rootless"])
            check_type(argname="argument schedulername", value=schedulername, expected_type=type_hints["schedulername"])
            check_type(argname="argument serviceaccount", value=serviceaccount, expected_type=type_hints["serviceaccount"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tolerations", value=tolerations, expected_type=type_hints["tolerations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if default_load is not None:
            self._values["default_load"] = default_load
        if image is not None:
            self._values["image"] = image
        if labels is not None:
            self._values["labels"] = labels
        if limits is not None:
            self._values["limits"] = limits
        if loadbalance is not None:
            self._values["loadbalance"] = loadbalance
        if namespace is not None:
            self._values["namespace"] = namespace
        if nodeselector is not None:
            self._values["nodeselector"] = nodeselector
        if qemu is not None:
            self._values["qemu"] = qemu
        if replicas is not None:
            self._values["replicas"] = replicas
        if requests is not None:
            self._values["requests"] = requests
        if rootless is not None:
            self._values["rootless"] = rootless
        if schedulername is not None:
            self._values["schedulername"] = schedulername
        if serviceaccount is not None:
            self._values["serviceaccount"] = serviceaccount
        if timeout is not None:
            self._values["timeout"] = timeout
        if tolerations is not None:
            self._values["tolerations"] = tolerations

    @builtins.property
    def annotations(self) -> typing.Optional[builtins.str]:
        '''Sets additional annotations on the deployments and pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#annotations BuildxBuilder#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_load(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically load images to the Docker Engine image store. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        '''
        result = self._values.get("default_load")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Sets the image to use for running BuildKit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[builtins.str]:
        '''Sets additional labels on the deployments and pods.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#labels BuildxBuilder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limits(self) -> typing.Optional["BuildxBuilderKubernetesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#limits BuildxBuilder#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["BuildxBuilderKubernetesLimits"], result)

    @builtins.property
    def loadbalance(self) -> typing.Optional[builtins.str]:
        '''Load-balancing strategy (sticky or random).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#loadbalance BuildxBuilder#loadbalance}
        '''
        result = self._values.get("loadbalance")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Sets the Kubernetes namespace.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#namespace BuildxBuilder#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodeselector(self) -> typing.Optional[builtins.str]:
        '''Sets the pod's nodeSelector label(s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#nodeselector BuildxBuilder#nodeselector}
        '''
        result = self._values.get("nodeselector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qemu(self) -> typing.Optional["BuildxBuilderKubernetesQemu"]:
        '''qemu block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#qemu BuildxBuilder#qemu}
        '''
        result = self._values.get("qemu")
        return typing.cast(typing.Optional["BuildxBuilderKubernetesQemu"], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''Sets the number of Pod replicas to create.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#replicas BuildxBuilder#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def requests(self) -> typing.Optional["BuildxBuilderKubernetesRequests"]:
        '''requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#requests BuildxBuilder#requests}
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional["BuildxBuilderKubernetesRequests"], result)

    @builtins.property
    def rootless(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Run the container as a non-root user.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#rootless BuildxBuilder#rootless}
        '''
        result = self._values.get("rootless")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def schedulername(self) -> typing.Optional[builtins.str]:
        '''Sets the scheduler responsible for scheduling the pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#schedulername BuildxBuilder#schedulername}
        '''
        result = self._values.get("schedulername")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serviceaccount(self) -> typing.Optional[builtins.str]:
        '''Sets the pod's serviceAccountName.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#serviceaccount BuildxBuilder#serviceaccount}
        '''
        result = self._values.get("serviceaccount")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Set the timeout limit for pod provisioning.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#timeout BuildxBuilder#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tolerations(self) -> typing.Optional[builtins.str]:
        '''Configures the pod's taint toleration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#tolerations BuildxBuilder#tolerations}
        '''
        result = self._values.get("tolerations")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderKubernetes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesLimits",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "ephemeral_storage": "ephemeralStorage",
        "memory": "memory",
    },
)
class BuildxBuilderKubernetesLimits:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        :param ephemeral_storage: Ephemeral storage limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        :param memory: Memory limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1335a713c8bd36d924cfa918f66c0da402f95ef735e4bcfb8c2c6acfff9cc4b0)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''CPU limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_storage(self) -> typing.Optional[builtins.str]:
        '''Ephemeral storage limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderKubernetesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildxBuilderKubernetesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesLimitsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d945b0b3e34c86eae160a49921b740620f780e0d9cbed940e2eb71646ac1fdeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62c731f718f4b9c520d107f26666c6a71cf3b520127bf5b19ae107b132b20fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @ephemeral_storage.setter
    def ephemeral_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037a774db3ad48805fffa6267a62472ceb320d212adf6baa89f96c7752bafc3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ephemeralStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee0728ad6e7bff32ed83dd08ed5f034dfa706be4d4a3329582ce6ec381cdf3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderKubernetesLimits]:
        return typing.cast(typing.Optional[BuildxBuilderKubernetesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BuildxBuilderKubernetesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a5c6adc1561438139edcd6f3313f56bf44212ae3d82efe0fbfd31d9359a962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BuildxBuilderKubernetesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591b1f202d887bbc340b988f71fbe6be7299072c5b0c4059aa113d02d2831521)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        :param ephemeral_storage: Ephemeral storage limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        :param memory: Memory limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        value = BuildxBuilderKubernetesLimits(
            cpu=cpu, ephemeral_storage=ephemeral_storage, memory=memory
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putQemu")
    def put_qemu(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        install: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param image: Sets the QEMU emulation image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param install: Install QEMU emulation for multi-platform support. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#install BuildxBuilder#install}
        '''
        value = BuildxBuilderKubernetesQemu(image=image, install=install)

        return typing.cast(None, jsii.invoke(self, "putQemu", [value]))

    @jsii.member(jsii_name="putRequests")
    def put_requests(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        :param ephemeral_storage: Ephemeral storage limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        :param memory: Memory limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        value = BuildxBuilderKubernetesRequests(
            cpu=cpu, ephemeral_storage=ephemeral_storage, memory=memory
        )

        return typing.cast(None, jsii.invoke(self, "putRequests", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDefaultLoad")
    def reset_default_load(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLoad", []))

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetLoadbalance")
    def reset_loadbalance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadbalance", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetNodeselector")
    def reset_nodeselector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeselector", []))

    @jsii.member(jsii_name="resetQemu")
    def reset_qemu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQemu", []))

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @jsii.member(jsii_name="resetRequests")
    def reset_requests(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequests", []))

    @jsii.member(jsii_name="resetRootless")
    def reset_rootless(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootless", []))

    @jsii.member(jsii_name="resetSchedulername")
    def reset_schedulername(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedulername", []))

    @jsii.member(jsii_name="resetServiceaccount")
    def reset_serviceaccount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceaccount", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTolerations")
    def reset_tolerations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTolerations", []))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> BuildxBuilderKubernetesLimitsOutputReference:
        return typing.cast(BuildxBuilderKubernetesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="qemu")
    def qemu(self) -> "BuildxBuilderKubernetesQemuOutputReference":
        return typing.cast("BuildxBuilderKubernetesQemuOutputReference", jsii.get(self, "qemu"))

    @builtins.property
    @jsii.member(jsii_name="requests")
    def requests(self) -> "BuildxBuilderKubernetesRequestsOutputReference":
        return typing.cast("BuildxBuilderKubernetesRequestsOutputReference", jsii.get(self, "requests"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLoadInput")
    def default_load_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultLoadInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(self) -> typing.Optional[BuildxBuilderKubernetesLimits]:
        return typing.cast(typing.Optional[BuildxBuilderKubernetesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="loadbalanceInput")
    def loadbalance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadbalanceInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeselectorInput")
    def nodeselector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeselectorInput"))

    @builtins.property
    @jsii.member(jsii_name="qemuInput")
    def qemu_input(self) -> typing.Optional["BuildxBuilderKubernetesQemu"]:
        return typing.cast(typing.Optional["BuildxBuilderKubernetesQemu"], jsii.get(self, "qemuInput"))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="requestsInput")
    def requests_input(self) -> typing.Optional["BuildxBuilderKubernetesRequests"]:
        return typing.cast(typing.Optional["BuildxBuilderKubernetesRequests"], jsii.get(self, "requestsInput"))

    @builtins.property
    @jsii.member(jsii_name="rootlessInput")
    def rootless_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootlessInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulernameInput")
    def schedulername_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedulernameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceaccountInput")
    def serviceaccount_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceaccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="tolerationsInput")
    def tolerations_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tolerationsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7fc32179d7b88f31766d690ed7634f24b50e87054cb49538e3c281babdcd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLoad")
    def default_load(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultLoad"))

    @default_load.setter
    def default_load(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd561ab58e4c4021b652d8c4c0cb585889fb8bb168cc714767e73163d16fe6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLoad", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b70fdb5edb598726145e17dcaa80bbfe74675e1a19ac2aec40b1168e1993bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53b6a2d39325b30ebd984522b8962e2f92ca8b34a673517ee884260ff6249e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadbalance")
    def loadbalance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadbalance"))

    @loadbalance.setter
    def loadbalance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cce18c65f6a57e977986c576cf616ef126f7f624ec08eb2603d2ac17738b738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadbalance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6418208f13a62d938955415a49c9c59dd4c3a2a550106f9eea7135959f953f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeselector")
    def nodeselector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeselector"))

    @nodeselector.setter
    def nodeselector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415e1b4d9ad3eafd32301375c2ddaf79f617471f77031d567ffb36035e80f93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeselector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04dd714f058a8d31a4cb30168779a1db75ea8900feb985c042a9ce2cd12984a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootless")
    def rootless(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootless"))

    @rootless.setter
    def rootless(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68addd262079a54fdc25bb8fa4ba49de77b14e3b61258e8e4d06f412fffbac3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootless", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedulername")
    def schedulername(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedulername"))

    @schedulername.setter
    def schedulername(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4b4315629cd5e9ee266e408fabfc1d7df5ab46af38dad1b87bc8f1904a357e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceaccount")
    def serviceaccount(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceaccount"))

    @serviceaccount.setter
    def serviceaccount(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6a7d29329a51260a819ac89a3c99b95b7cfa84c6c0dbeb785a32bc12a8d1a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceaccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f3a8bde143e7d5a5be4363a409d921027deb9fc0a750267c4bcf6393cdf619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tolerations")
    def tolerations(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tolerations"))

    @tolerations.setter
    def tolerations(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__083066122a9a6dad87daa800079156577136f21f2ca37bb0e8fa7876ac66f345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tolerations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderKubernetes]:
        return typing.cast(typing.Optional[BuildxBuilderKubernetes], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BuildxBuilderKubernetes]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e7c6054cdc857d64c008b08280261b5c654af1c19771e03b83c48fe31bbc945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesQemu",
    jsii_struct_bases=[],
    name_mapping={"image": "image", "install": "install"},
)
class BuildxBuilderKubernetesQemu:
    def __init__(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        install: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param image: Sets the QEMU emulation image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        :param install: Install QEMU emulation for multi-platform support. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#install BuildxBuilder#install}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68137972f74d58587ec55450e239e80e3ea2cdfee46214a8aa692ced9948f6e5)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument install", value=install, expected_type=type_hints["install"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if install is not None:
            self._values["install"] = install

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Sets the QEMU emulation image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#image BuildxBuilder#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Install QEMU emulation for multi-platform support.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#install BuildxBuilder#install}
        '''
        result = self._values.get("install")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderKubernetesQemu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildxBuilderKubernetesQemuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesQemuOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff8e27dae8d05def97fbec08ab0957eadb6ee5bfecfa57ef2e3cd95d877edd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetInstall")
    def reset_install(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstall", []))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="installInput")
    def install_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "installInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf99df557710ccd44d08dc24b9a942affe7431d87d636ca628097fe706597600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="install")
    def install(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "install"))

    @install.setter
    def install(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849228f91db615341ebb27e24e8587a84faafdcf43e9278771dda477cbd6f6e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "install", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderKubernetesQemu]:
        return typing.cast(typing.Optional[BuildxBuilderKubernetesQemu], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BuildxBuilderKubernetesQemu],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00abca1cbe15b01fa99d61e98b4d0babc3f5a6f4996ac0232e622e5473dd5d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesRequests",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "ephemeral_storage": "ephemeralStorage",
        "memory": "memory",
    },
)
class BuildxBuilderKubernetesRequests:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: CPU limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        :param ephemeral_storage: Ephemeral storage limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        :param memory: Memory limit for the Kubernetes pod. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d8b57838f7ae5ad521efe400fc9920c882d978c44a209627d9b440c7d405c8)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''CPU limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cpu BuildxBuilder#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_storage(self) -> typing.Optional[builtins.str]:
        '''Ephemeral storage limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#ephemeral_storage BuildxBuilder#ephemeral_storage}
        '''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''Memory limit for the Kubernetes pod.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#memory BuildxBuilder#memory}
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderKubernetesRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildxBuilderKubernetesRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderKubernetesRequestsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3cbf566e6011ea609a005f616ef992d865e12972c7b554d67c04a95490a5a3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cpu"))

    @cpu.setter
    def cpu(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f17a48fc820e48ccbbf512d1284050cadc490c99bc1bf8dea39fbf2b117777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ephemeralStorage"))

    @ephemeral_storage.setter
    def ephemeral_storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__529e10222af7041331aa7d4161cf5267333f8f0308f32750c6aff88d7635b006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ephemeralStorage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "memory"))

    @memory.setter
    def memory(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66d0f2b44194b483f634c05dee87d105cf866d33d89ed1c25c60f9b17a4ba83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memory", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderKubernetesRequests]:
        return typing.cast(typing.Optional[BuildxBuilderKubernetesRequests], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BuildxBuilderKubernetesRequests],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecc3701722f11430ab57c932b8abdaa3fb33df3514a4dee3a7ae95571f55099)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderRemote",
    jsii_struct_bases=[],
    name_mapping={
        "cacert": "cacert",
        "cert": "cert",
        "default_load": "defaultLoad",
        "key": "key",
        "servername": "servername",
    },
)
class BuildxBuilderRemote:
    def __init__(
        self,
        *,
        cacert: typing.Optional[builtins.str] = None,
        cert: typing.Optional[builtins.str] = None,
        default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        key: typing.Optional[builtins.str] = None,
        servername: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cacert: Absolute path to the TLS certificate authority used for validation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cacert BuildxBuilder#cacert}
        :param cert: Absolute path to the TLS client certificate to present to buildkitd. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cert BuildxBuilder#cert}
        :param default_load: Automatically load images to the Docker Engine image store. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        :param key: Sets the TLS client key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#key BuildxBuilder#key}
        :param servername: TLS server name used in requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#servername BuildxBuilder#servername}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2970f9c40d72e588e73b81b37f5543de92eee3db2f2d372f8178c3f9040f9f3)
            check_type(argname="argument cacert", value=cacert, expected_type=type_hints["cacert"])
            check_type(argname="argument cert", value=cert, expected_type=type_hints["cert"])
            check_type(argname="argument default_load", value=default_load, expected_type=type_hints["default_load"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument servername", value=servername, expected_type=type_hints["servername"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cacert is not None:
            self._values["cacert"] = cacert
        if cert is not None:
            self._values["cert"] = cert
        if default_load is not None:
            self._values["default_load"] = default_load
        if key is not None:
            self._values["key"] = key
        if servername is not None:
            self._values["servername"] = servername

    @builtins.property
    def cacert(self) -> typing.Optional[builtins.str]:
        '''Absolute path to the TLS certificate authority used for validation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cacert BuildxBuilder#cacert}
        '''
        result = self._values.get("cacert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cert(self) -> typing.Optional[builtins.str]:
        '''Absolute path to the TLS client certificate to present to buildkitd.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#cert BuildxBuilder#cert}
        '''
        result = self._values.get("cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_load(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatically load images to the Docker Engine image store. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#default_load BuildxBuilder#default_load}
        '''
        result = self._values.get("default_load")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Sets the TLS client key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#key BuildxBuilder#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servername(self) -> typing.Optional[builtins.str]:
        '''TLS server name used in requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/buildx_builder#servername BuildxBuilder#servername}
        '''
        result = self._values.get("servername")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildxBuilderRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildxBuilderRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.buildxBuilder.BuildxBuilderRemoteOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d20a53fba97acbd34eb667759a4b53a9f5342eb8e9ddb7833f62df324883b3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCacert")
    def reset_cacert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCacert", []))

    @jsii.member(jsii_name="resetCert")
    def reset_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCert", []))

    @jsii.member(jsii_name="resetDefaultLoad")
    def reset_default_load(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLoad", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetServername")
    def reset_servername(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServername", []))

    @builtins.property
    @jsii.member(jsii_name="cacertInput")
    def cacert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacertInput"))

    @builtins.property
    @jsii.member(jsii_name="certInput")
    def cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLoadInput")
    def default_load_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultLoadInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="servernameInput")
    def servername_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servernameInput"))

    @builtins.property
    @jsii.member(jsii_name="cacert")
    def cacert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacert"))

    @cacert.setter
    def cacert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7e4fe97ba158cb22c1908f1abbd6afb99a27c2a5b2458e77b901ee679f2577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cert")
    def cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cert"))

    @cert.setter
    def cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1845b6a70d20743aa9361f11a77e3bd60cec561cb9924c1f55efd337e9e05b6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cert", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultLoad")
    def default_load(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultLoad"))

    @default_load.setter
    def default_load(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17cd67ce41e306e303b94531206cb5b324dff35e2505307ae7a96f80e117029d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLoad", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24054d62b772a5f9bea2d28acab40993ffbea0f1d827d2d59d32acaf14544930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servername")
    def servername(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servername"))

    @servername.setter
    def servername(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7131c8e5a7e6cfaefb06dc376482363b5a86f55311803f86d9919de2b435a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BuildxBuilderRemote]:
        return typing.cast(typing.Optional[BuildxBuilderRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[BuildxBuilderRemote]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154c45784e9ba03b0377e74460340ad0b59f958b89791afb3d760d0bec934d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BuildxBuilder",
    "BuildxBuilderConfig",
    "BuildxBuilderDockerContainer",
    "BuildxBuilderDockerContainerOutputReference",
    "BuildxBuilderKubernetes",
    "BuildxBuilderKubernetesLimits",
    "BuildxBuilderKubernetesLimitsOutputReference",
    "BuildxBuilderKubernetesOutputReference",
    "BuildxBuilderKubernetesQemu",
    "BuildxBuilderKubernetesQemuOutputReference",
    "BuildxBuilderKubernetesRequests",
    "BuildxBuilderKubernetesRequestsOutputReference",
    "BuildxBuilderRemote",
    "BuildxBuilderRemoteOutputReference",
]

publication.publish()

def _typecheckingstub__e978ee7de1168113840100daaaff2a947d447d222d6e0e4ba5a5163072495d6a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bootstrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    buildkit_config: typing.Optional[builtins.str] = None,
    buildkit_flags: typing.Optional[builtins.str] = None,
    docker_container: typing.Optional[typing.Union[BuildxBuilderDockerContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    driver: typing.Optional[builtins.str] = None,
    driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes: typing.Optional[typing.Union[BuildxBuilderKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_attribute: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote: typing.Optional[typing.Union[BuildxBuilderRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    use: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96fbc7092fd63dd79e99304ec952e7339f71902fc424eb832a85834bb6821cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe50460855baebf4b73542e7b7f18776cfd505934e0c274a53b500f576f542c9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d337a347946d3f01eefa8ce1fc90c4681d2054262cf8f46e7e6cc04a5c9754f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d96356b227e5342fd922d3521e41a32cd96e7bc5018cb6024c3519e660641ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efae3d395316e86aee85b289529041b1eaf57f9ddd2d5c518915ee9fc577c945(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2fca5a0e7be0af9c8f77e2ee11a870d57f698d056e6dbaedf110fec6a2b740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e350f4f840bbac9f5d323d5a17b4edee95665a0d66b4c764bac7ecdbf6caca0b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ab7b2c137f5aa251931206fb374a6bf870c3a12a5c53fd8abd50bc1e1bab36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e420a7d6f04ebb97786186678e3435ff8cda41e94b0aefa23daf49489a7abc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c1471f95f73a87697704efe80b3cdb3e782649ac13f8454dc3728d571ebd0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4067cbe098e507978ce489692c9d240985994f83791d0984540debe7dd6401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75612131a54bed960843b3c7b9abee07f2564334a982c41a5725c4cc74f6e2b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26531bf84b6598761a5a9760aa54b7a2feffbee1411e0f730a8a64344a8cfd0d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552c4b130918a9743da4e84ba6082a1ce269edaffb52d4be17497a5125432afe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    append: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bootstrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    buildkit_config: typing.Optional[builtins.str] = None,
    buildkit_flags: typing.Optional[builtins.str] = None,
    docker_container: typing.Optional[typing.Union[BuildxBuilderDockerContainer, typing.Dict[builtins.str, typing.Any]]] = None,
    driver: typing.Optional[builtins.str] = None,
    driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    endpoint: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kubernetes: typing.Optional[typing.Union[BuildxBuilderKubernetes, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    node_attribute: typing.Optional[builtins.str] = None,
    platform: typing.Optional[typing.Sequence[builtins.str]] = None,
    remote: typing.Optional[typing.Union[BuildxBuilderRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    use: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dbd7239a186057cb9ccfadf91f8c61a32c36702ef8a07f9b1cdc9506351344(
    *,
    cgroup_parent: typing.Optional[builtins.str] = None,
    cpu_period: typing.Optional[builtins.str] = None,
    cpu_quota: typing.Optional[builtins.str] = None,
    cpuset_cpus: typing.Optional[builtins.str] = None,
    cpuset_mems: typing.Optional[builtins.str] = None,
    cpu_shares: typing.Optional[builtins.str] = None,
    default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
    memory_swap: typing.Optional[builtins.str] = None,
    network: typing.Optional[builtins.str] = None,
    restart_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2cb7e870463bca5c08f1b1d6cf57eb7971e59e1a067ff32d89b37ab1c12c691(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33651599c3212198fd5334b5919f1f850851f00511461eaa00f00985355f5291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5598b7e9e56a2d87fa58d5efe84f288b3f81de8671f0d69aa5aa737161070c77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b498cd2559bdac7810133f21df6f5733b0339380d8f59365479628d39654891c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2f31ea5994040a7f03edc6f5cf335e335b00f4683c5314d1a5603f94f35962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520ba5545304f041f47eefa2c9f670cb77a53496d9d0a8fc1722fea48f0a6390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d66ec8181dc1adcd88d966b335170487f0a7ad554f77d3dce7a7781629b2f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1555fd2d2bc7cbedfe21fac886eff84febe5dbd6aa72e86a020aa979ad06914e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b475b4536ff0a91bfdf19c8b1635f3492c5a97fad63baca33b3ed3d9196170(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6625f3e7a846df5c4a657c53a6e97a6f3e608f76980f42fcd622a28247dbaec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3642129eb3b452648de477ea348cbeda3f03fa43242e9480445215d7f935ef68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce20d79c2f1ba22efcc30b8ac0fa6039cb6f303faf0df667188ed1b0d53a3bd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aed8e3c9b73fae852ce48dc035134b2ad311b5d56a4d7e167882abfed6282c57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbf1acede18eb59c04722332dc330d5f6bf7272bb8fea8ce901b3d167f9777c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3e386e51fc29cbdbcd61e9a5b6928ec4ced49ce56f261bba9477c2a07b9978(
    value: typing.Optional[BuildxBuilderDockerContainer],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f99aa3085ef502e08a7c188bb97a44ba8b8030869fcae887f44497bf49d297(
    *,
    annotations: typing.Optional[builtins.str] = None,
    default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    image: typing.Optional[builtins.str] = None,
    labels: typing.Optional[builtins.str] = None,
    limits: typing.Optional[typing.Union[BuildxBuilderKubernetesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    loadbalance: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    nodeselector: typing.Optional[builtins.str] = None,
    qemu: typing.Optional[typing.Union[BuildxBuilderKubernetesQemu, typing.Dict[builtins.str, typing.Any]]] = None,
    replicas: typing.Optional[jsii.Number] = None,
    requests: typing.Optional[typing.Union[BuildxBuilderKubernetesRequests, typing.Dict[builtins.str, typing.Any]]] = None,
    rootless: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    schedulername: typing.Optional[builtins.str] = None,
    serviceaccount: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
    tolerations: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1335a713c8bd36d924cfa918f66c0da402f95ef735e4bcfb8c2c6acfff9cc4b0(
    *,
    cpu: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d945b0b3e34c86eae160a49921b740620f780e0d9cbed940e2eb71646ac1fdeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62c731f718f4b9c520d107f26666c6a71cf3b520127bf5b19ae107b132b20fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037a774db3ad48805fffa6267a62472ceb320d212adf6baa89f96c7752bafc3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee0728ad6e7bff32ed83dd08ed5f034dfa706be4d4a3329582ce6ec381cdf3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a5c6adc1561438139edcd6f3313f56bf44212ae3d82efe0fbfd31d9359a962(
    value: typing.Optional[BuildxBuilderKubernetesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591b1f202d887bbc340b988f71fbe6be7299072c5b0c4059aa113d02d2831521(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7fc32179d7b88f31766d690ed7634f24b50e87054cb49538e3c281babdcd47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd561ab58e4c4021b652d8c4c0cb585889fb8bb168cc714767e73163d16fe6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b70fdb5edb598726145e17dcaa80bbfe74675e1a19ac2aec40b1168e1993bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53b6a2d39325b30ebd984522b8962e2f92ca8b34a673517ee884260ff6249e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cce18c65f6a57e977986c576cf616ef126f7f624ec08eb2603d2ac17738b738(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6418208f13a62d938955415a49c9c59dd4c3a2a550106f9eea7135959f953f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415e1b4d9ad3eafd32301375c2ddaf79f617471f77031d567ffb36035e80f93c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04dd714f058a8d31a4cb30168779a1db75ea8900feb985c042a9ce2cd12984a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68addd262079a54fdc25bb8fa4ba49de77b14e3b61258e8e4d06f412fffbac3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b4315629cd5e9ee266e408fabfc1d7df5ab46af38dad1b87bc8f1904a357e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6a7d29329a51260a819ac89a3c99b95b7cfa84c6c0dbeb785a32bc12a8d1a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f3a8bde143e7d5a5be4363a409d921027deb9fc0a750267c4bcf6393cdf619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083066122a9a6dad87daa800079156577136f21f2ca37bb0e8fa7876ac66f345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e7c6054cdc857d64c008b08280261b5c654af1c19771e03b83c48fe31bbc945(
    value: typing.Optional[BuildxBuilderKubernetes],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68137972f74d58587ec55450e239e80e3ea2cdfee46214a8aa692ced9948f6e5(
    *,
    image: typing.Optional[builtins.str] = None,
    install: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff8e27dae8d05def97fbec08ab0957eadb6ee5bfecfa57ef2e3cd95d877edd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf99df557710ccd44d08dc24b9a942affe7431d87d636ca628097fe706597600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849228f91db615341ebb27e24e8587a84faafdcf43e9278771dda477cbd6f6e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00abca1cbe15b01fa99d61e98b4d0babc3f5a6f4996ac0232e622e5473dd5d5e(
    value: typing.Optional[BuildxBuilderKubernetesQemu],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d8b57838f7ae5ad521efe400fc9920c882d978c44a209627d9b440c7d405c8(
    *,
    cpu: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[builtins.str] = None,
    memory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cbf566e6011ea609a005f616ef992d865e12972c7b554d67c04a95490a5a3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f17a48fc820e48ccbbf512d1284050cadc490c99bc1bf8dea39fbf2b117777(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529e10222af7041331aa7d4161cf5267333f8f0308f32750c6aff88d7635b006(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66d0f2b44194b483f634c05dee87d105cf866d33d89ed1c25c60f9b17a4ba83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecc3701722f11430ab57c932b8abdaa3fb33df3514a4dee3a7ae95571f55099(
    value: typing.Optional[BuildxBuilderKubernetesRequests],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2970f9c40d72e588e73b81b37f5543de92eee3db2f2d372f8178c3f9040f9f3(
    *,
    cacert: typing.Optional[builtins.str] = None,
    cert: typing.Optional[builtins.str] = None,
    default_load: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    key: typing.Optional[builtins.str] = None,
    servername: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d20a53fba97acbd34eb667759a4b53a9f5342eb8e9ddb7833f62df324883b3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7e4fe97ba158cb22c1908f1abbd6afb99a27c2a5b2458e77b901ee679f2577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1845b6a70d20743aa9361f11a77e3bd60cec561cb9924c1f55efd337e9e05b6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cd67ce41e306e303b94531206cb5b324dff35e2505307ae7a96f80e117029d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24054d62b772a5f9bea2d28acab40993ffbea0f1d827d2d59d32acaf14544930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7131c8e5a7e6cfaefb06dc376482363b5a86f55311803f86d9919de2b435a0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154c45784e9ba03b0377e74460340ad0b59f958b89791afb3d760d0bec934d70(
    value: typing.Optional[BuildxBuilderRemote],
) -> None:
    """Type checking stubs"""
    pass
