r'''
# `docker_service`

Refer to the Terraform Registry for docs: [`docker_service`](https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service).
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


class Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service docker_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        task_spec: typing.Union["ServiceTaskSpec", typing.Dict[builtins.str, typing.Any]],
        auth: typing.Optional[typing.Union["ServiceAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        converge_config: typing.Optional[typing.Union["ServiceConvergeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_spec: typing.Optional[typing.Union["ServiceEndpointSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[typing.Union["ServiceMode", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback_config: typing.Optional[typing.Union["ServiceRollbackConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["ServiceUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service docker_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param task_spec: task_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#task_spec Service#task_spec}
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#auth Service#auth}
        :param converge_config: converge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#converge_config Service#converge_config}
        :param endpoint_spec: endpoint_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#endpoint_spec Service#endpoint_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param mode: mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param rollback_config: rollback_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#rollback_config Service#rollback_config}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#update_config Service#update_config}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cb49c196354f919c566ae3e0ffcea09c2682023510f1ba79d99f59317958fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceConfig(
            name=name,
            task_spec=task_spec,
            auth=auth,
            converge_config=converge_config,
            endpoint_spec=endpoint_spec,
            id=id,
            labels=labels,
            mode=mode,
            rollback_config=rollback_config,
            update_config=update_config,
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
        '''Generates CDKTF code for importing a Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Service to import.
        :param import_from_id: The id of the existing Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6762d0eba2e4fa258cedd385e5cfe12774d754bac429e647c967de743af5c25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuth")
    def put_auth(
        self,
        *,
        server_address: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_address: The address of the server for the authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#server_address Service#server_address}
        :param password: The password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#password Service#password}
        :param username: The username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#username Service#username}
        '''
        value = ServiceAuth(
            server_address=server_address, password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putAuth", [value]))

    @jsii.member(jsii_name="putConvergeConfig")
    def put_converge_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delay: The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param timeout: The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        value = ServiceConvergeConfig(delay=delay, timeout=timeout)

        return typing.cast(None, jsii.invoke(self, "putConvergeConfig", [value]))

    @jsii.member(jsii_name="putEndpointSpec")
    def put_endpoint_spec(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of resolution to use for internal load balancing between tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#ports Service#ports}
        '''
        value = ServiceEndpointSpec(mode=mode, ports=ports)

        return typing.cast(None, jsii.invoke(self, "putEndpointSpec", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c4e04342a7e60f6f14ca6abf03cc34722629bc87370808312b5dfb16369d309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putMode")
    def put_mode(
        self,
        *,
        global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicated: typing.Optional[typing.Union["ServiceModeReplicated", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param global_: The global service mode. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#global Service#global}
        :param replicated: replicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicated Service#replicated}
        '''
        value = ServiceMode(global_=global_, replicated=replicated)

        return typing.cast(None, jsii.invoke(self, "putMode", [value]))

    @jsii.member(jsii_name="putRollbackConfig")
    def put_rollback_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param failure_action: Action on rollback failure: pause | continue. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during a rollback. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        :param order: Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        value = ServiceRollbackConfig(
            delay=delay,
            failure_action=failure_action,
            max_failure_ratio=max_failure_ratio,
            monitor=monitor,
            order=order,
            parallelism=parallelism,
        )

        return typing.cast(None, jsii.invoke(self, "putRollbackConfig", [value]))

    @jsii.member(jsii_name="putTaskSpec")
    def put_task_spec(
        self,
        *,
        container_spec: typing.Union["ServiceTaskSpecContainerSpec", typing.Dict[builtins.str, typing.Any]],
        force_update: typing.Optional[jsii.Number] = None,
        log_driver: typing.Optional[typing.Union["ServiceTaskSpecLogDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement: typing.Optional[typing.Union["ServiceTaskSpecPlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["ServiceTaskSpecResources", typing.Dict[builtins.str, typing.Any]]] = None,
        restart_policy: typing.Optional[typing.Union["ServiceTaskSpecRestartPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#container_spec Service#container_spec}
        :param force_update: A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#force_update Service#force_update}
        :param log_driver: log_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#log_driver Service#log_driver}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#networks_advanced Service#networks_advanced}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#placement Service#placement}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#resources Service#resources}
        :param restart_policy: restart_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#restart_policy Service#restart_policy}
        :param runtime: Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#runtime Service#runtime}
        '''
        value = ServiceTaskSpec(
            container_spec=container_spec,
            force_update=force_update,
            log_driver=log_driver,
            networks_advanced=networks_advanced,
            placement=placement,
            resources=resources,
            restart_policy=restart_policy,
            runtime=runtime,
        )

        return typing.cast(None, jsii.invoke(self, "putTaskSpec", [value]))

    @jsii.member(jsii_name="putUpdateConfig")
    def put_update_config(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param failure_action: Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during an update. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        :param order: Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be updated in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        value = ServiceUpdateConfig(
            delay=delay,
            failure_action=failure_action,
            max_failure_ratio=max_failure_ratio,
            monitor=monitor,
            order=order,
            parallelism=parallelism,
        )

        return typing.cast(None, jsii.invoke(self, "putUpdateConfig", [value]))

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetConvergeConfig")
    def reset_converge_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConvergeConfig", []))

    @jsii.member(jsii_name="resetEndpointSpec")
    def reset_endpoint_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetRollbackConfig")
    def reset_rollback_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRollbackConfig", []))

    @jsii.member(jsii_name="resetUpdateConfig")
    def reset_update_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateConfig", []))

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
    @jsii.member(jsii_name="auth")
    def auth(self) -> "ServiceAuthOutputReference":
        return typing.cast("ServiceAuthOutputReference", jsii.get(self, "auth"))

    @builtins.property
    @jsii.member(jsii_name="convergeConfig")
    def converge_config(self) -> "ServiceConvergeConfigOutputReference":
        return typing.cast("ServiceConvergeConfigOutputReference", jsii.get(self, "convergeConfig"))

    @builtins.property
    @jsii.member(jsii_name="endpointSpec")
    def endpoint_spec(self) -> "ServiceEndpointSpecOutputReference":
        return typing.cast("ServiceEndpointSpecOutputReference", jsii.get(self, "endpointSpec"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> "ServiceLabelsList":
        return typing.cast("ServiceLabelsList", jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> "ServiceModeOutputReference":
        return typing.cast("ServiceModeOutputReference", jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="rollbackConfig")
    def rollback_config(self) -> "ServiceRollbackConfigOutputReference":
        return typing.cast("ServiceRollbackConfigOutputReference", jsii.get(self, "rollbackConfig"))

    @builtins.property
    @jsii.member(jsii_name="taskSpec")
    def task_spec(self) -> "ServiceTaskSpecOutputReference":
        return typing.cast("ServiceTaskSpecOutputReference", jsii.get(self, "taskSpec"))

    @builtins.property
    @jsii.member(jsii_name="updateConfig")
    def update_config(self) -> "ServiceUpdateConfigOutputReference":
        return typing.cast("ServiceUpdateConfigOutputReference", jsii.get(self, "updateConfig"))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional["ServiceAuth"]:
        return typing.cast(typing.Optional["ServiceAuth"], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="convergeConfigInput")
    def converge_config_input(self) -> typing.Optional["ServiceConvergeConfig"]:
        return typing.cast(typing.Optional["ServiceConvergeConfig"], jsii.get(self, "convergeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointSpecInput")
    def endpoint_spec_input(self) -> typing.Optional["ServiceEndpointSpec"]:
        return typing.cast(typing.Optional["ServiceEndpointSpec"], jsii.get(self, "endpointSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional["ServiceMode"]:
        return typing.cast(typing.Optional["ServiceMode"], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="rollbackConfigInput")
    def rollback_config_input(self) -> typing.Optional["ServiceRollbackConfig"]:
        return typing.cast(typing.Optional["ServiceRollbackConfig"], jsii.get(self, "rollbackConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="taskSpecInput")
    def task_spec_input(self) -> typing.Optional["ServiceTaskSpec"]:
        return typing.cast(typing.Optional["ServiceTaskSpec"], jsii.get(self, "taskSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="updateConfigInput")
    def update_config_input(self) -> typing.Optional["ServiceUpdateConfig"]:
        return typing.cast(typing.Optional["ServiceUpdateConfig"], jsii.get(self, "updateConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6522b7f59cb6f5199e43d6472fc36d6a9fb8ed44ed04775ce7988a5f6b6a2a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f026f3c5bd7c094670284db6f25f343a09da1d8d73e64c56e6b6e2bab8ad81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceAuth",
    jsii_struct_bases=[],
    name_mapping={
        "server_address": "serverAddress",
        "password": "password",
        "username": "username",
    },
)
class ServiceAuth:
    def __init__(
        self,
        *,
        server_address: builtins.str,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param server_address: The address of the server for the authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#server_address Service#server_address}
        :param password: The password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#password Service#password}
        :param username: The username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#username Service#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9aea760943cefe39bf2f4c67ea8caec4f9b38ceb027ee64faff5db46376b287)
            check_type(argname="argument server_address", value=server_address, expected_type=type_hints["server_address"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_address": server_address,
        }
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def server_address(self) -> builtins.str:
        '''The address of the server for the authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#server_address Service#server_address}
        '''
        result = self._values.get("server_address")
        assert result is not None, "Required property 'server_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#password Service#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#username Service#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9acd31ab3db0059f772cfe75ec4c0fc49c4cbe62ba4976f33553dbf73885b0d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverAddressInput")
    def server_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e88d9fdf235a7645e78c24c572906257dcb75d16c3884584121ca38bdda6fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverAddress")
    def server_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverAddress"))

    @server_address.setter
    def server_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ef46c0d34f114ce12109c552dc95b282d57ee21fee06de8866543c454434be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898e4d2e30e1392c7881d68eaf657ae9dbfd4c861b41cadd991b73d2e7b7ad63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceAuth]:
        return typing.cast(typing.Optional[ServiceAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceAuth]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39eb64684b9f0ecc2176aa86329077af1a112ca6a31fd983e22708e4df234e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "task_spec": "taskSpec",
        "auth": "auth",
        "converge_config": "convergeConfig",
        "endpoint_spec": "endpointSpec",
        "id": "id",
        "labels": "labels",
        "mode": "mode",
        "rollback_config": "rollbackConfig",
        "update_config": "updateConfig",
    },
)
class ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        task_spec: typing.Union["ServiceTaskSpec", typing.Dict[builtins.str, typing.Any]],
        auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
        converge_config: typing.Optional[typing.Union["ServiceConvergeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        endpoint_spec: typing.Optional[typing.Union["ServiceEndpointSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mode: typing.Optional[typing.Union["ServiceMode", typing.Dict[builtins.str, typing.Any]]] = None,
        rollback_config: typing.Optional[typing.Union["ServiceRollbackConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        update_config: typing.Optional[typing.Union["ServiceUpdateConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param task_spec: task_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#task_spec Service#task_spec}
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#auth Service#auth}
        :param converge_config: converge_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#converge_config Service#converge_config}
        :param endpoint_spec: endpoint_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#endpoint_spec Service#endpoint_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param mode: mode block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param rollback_config: rollback_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#rollback_config Service#rollback_config}
        :param update_config: update_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#update_config Service#update_config}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(task_spec, dict):
            task_spec = ServiceTaskSpec(**task_spec)
        if isinstance(auth, dict):
            auth = ServiceAuth(**auth)
        if isinstance(converge_config, dict):
            converge_config = ServiceConvergeConfig(**converge_config)
        if isinstance(endpoint_spec, dict):
            endpoint_spec = ServiceEndpointSpec(**endpoint_spec)
        if isinstance(mode, dict):
            mode = ServiceMode(**mode)
        if isinstance(rollback_config, dict):
            rollback_config = ServiceRollbackConfig(**rollback_config)
        if isinstance(update_config, dict):
            update_config = ServiceUpdateConfig(**update_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3e7ecb041d517789e27c0692550c575bf9c57bb66d494a38497590dc354904)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument task_spec", value=task_spec, expected_type=type_hints["task_spec"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument converge_config", value=converge_config, expected_type=type_hints["converge_config"])
            check_type(argname="argument endpoint_spec", value=endpoint_spec, expected_type=type_hints["endpoint_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument rollback_config", value=rollback_config, expected_type=type_hints["rollback_config"])
            check_type(argname="argument update_config", value=update_config, expected_type=type_hints["update_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "task_spec": task_spec,
        }
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
        if auth is not None:
            self._values["auth"] = auth
        if converge_config is not None:
            self._values["converge_config"] = converge_config
        if endpoint_spec is not None:
            self._values["endpoint_spec"] = endpoint_spec
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mode is not None:
            self._values["mode"] = mode
        if rollback_config is not None:
            self._values["rollback_config"] = rollback_config
        if update_config is not None:
            self._values["update_config"] = update_config

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
    def name(self) -> builtins.str:
        '''Name of the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_spec(self) -> "ServiceTaskSpec":
        '''task_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#task_spec Service#task_spec}
        '''
        result = self._values.get("task_spec")
        assert result is not None, "Required property 'task_spec' is missing"
        return typing.cast("ServiceTaskSpec", result)

    @builtins.property
    def auth(self) -> typing.Optional[ServiceAuth]:
        '''auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#auth Service#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[ServiceAuth], result)

    @builtins.property
    def converge_config(self) -> typing.Optional["ServiceConvergeConfig"]:
        '''converge_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#converge_config Service#converge_config}
        '''
        result = self._values.get("converge_config")
        return typing.cast(typing.Optional["ServiceConvergeConfig"], result)

    @builtins.property
    def endpoint_spec(self) -> typing.Optional["ServiceEndpointSpec"]:
        '''endpoint_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#endpoint_spec Service#endpoint_spec}
        '''
        result = self._values.get("endpoint_spec")
        return typing.cast(typing.Optional["ServiceEndpointSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#id Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceLabels"]]], result)

    @builtins.property
    def mode(self) -> typing.Optional["ServiceMode"]:
        '''mode block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional["ServiceMode"], result)

    @builtins.property
    def rollback_config(self) -> typing.Optional["ServiceRollbackConfig"]:
        '''rollback_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#rollback_config Service#rollback_config}
        '''
        result = self._values.get("rollback_config")
        return typing.cast(typing.Optional["ServiceRollbackConfig"], result)

    @builtins.property
    def update_config(self) -> typing.Optional["ServiceUpdateConfig"]:
        '''update_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#update_config Service#update_config}
        '''
        result = self._values.get("update_config")
        return typing.cast(typing.Optional["ServiceUpdateConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceConvergeConfig",
    jsii_struct_bases=[],
    name_mapping={"delay": "delay", "timeout": "timeout"},
)
class ServiceConvergeConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param delay: The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param timeout: The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23210ffc14b693ac1e355a456926323e83361f73dfb530d88acbb6134fc0d9c)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''The interval to check if the desired state is reached ``(ms|s)``. Defaults to ``7s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''The timeout of the service to reach the desired state ``(s|m)``. Defaults to ``3m``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConvergeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceConvergeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceConvergeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5831fc4f695b229dab50bbc733a72d14cfe132b5a3561d2db2917dcdb20907c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6317bbae03b08a624dcb552e4e668bd0db7f000f32f4d3e5242410cdf2eeed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b584aba92d1804e0e39b279fe17b0223cd3494973b2b7522d4a683a91544dd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceConvergeConfig]:
        return typing.cast(typing.Optional[ServiceConvergeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceConvergeConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e2795b6e36c0d57d96912a8cb27201ac1e463a444eddfa50249aa84145c35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceEndpointSpec",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "ports": "ports"},
)
class ServiceEndpointSpec:
    def __init__(
        self,
        *,
        mode: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param mode: The mode of resolution to use for internal load balancing between tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#ports Service#ports}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2556ea1982c3b1b57993776dab8b88c7c07e1449e2dfbd9fe683a33fd3db90)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''The mode of resolution to use for internal load balancing between tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#ports Service#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEndpointSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceEndpointSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0346c93556480682a560b3f49bafcdc20188046a43cb381b50daf1ffe0938fd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEndpointSpecPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dc998a167b2ee7cb34c1015cfeaec871930987184e224910f04aea24edee77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "ServiceEndpointSpecPortsList":
        return typing.cast("ServiceEndpointSpecPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEndpointSpecPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c6641f4caa9d1a3c01ca5262c9d23ec7b4ef3944cd02054eb424fdcf46dd4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceEndpointSpec]:
        return typing.cast(typing.Optional[ServiceEndpointSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceEndpointSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ad98d869fbfaace2a83cd718a298c1e18dd07fcc21d9fcb8346befc1d3ac56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceEndpointSpecPorts",
    jsii_struct_bases=[],
    name_mapping={
        "target_port": "targetPort",
        "name": "name",
        "protocol": "protocol",
        "published_port": "publishedPort",
        "publish_mode": "publishMode",
    },
)
class ServiceEndpointSpecPorts:
    def __init__(
        self,
        *,
        target_port: jsii.Number,
        name: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        published_port: typing.Optional[jsii.Number] = None,
        publish_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target_port: The port inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#target_port Service#target_port}
        :param name: A random name for the port. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param protocol: Rrepresents the protocol of a port: ``tcp``, ``udp`` or ``sctp``. Defaults to ``tcp``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#protocol Service#protocol}
        :param published_port: The port on the swarm hosts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#published_port Service#published_port}
        :param publish_mode: Represents the mode in which the port is to be published: 'ingress' or 'host'. Defaults to ``ingress``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#publish_mode Service#publish_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd409048b41082aafae84395c8220721d026ea9efcfd6c94010ab472be15877)
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument published_port", value=published_port, expected_type=type_hints["published_port"])
            check_type(argname="argument publish_mode", value=publish_mode, expected_type=type_hints["publish_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_port": target_port,
        }
        if name is not None:
            self._values["name"] = name
        if protocol is not None:
            self._values["protocol"] = protocol
        if published_port is not None:
            self._values["published_port"] = published_port
        if publish_mode is not None:
            self._values["publish_mode"] = publish_mode

    @builtins.property
    def target_port(self) -> jsii.Number:
        '''The port inside the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#target_port Service#target_port}
        '''
        result = self._values.get("target_port")
        assert result is not None, "Required property 'target_port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A random name for the port.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Rrepresents the protocol of a port: ``tcp``, ``udp`` or ``sctp``. Defaults to ``tcp``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#protocol Service#protocol}
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def published_port(self) -> typing.Optional[jsii.Number]:
        '''The port on the swarm hosts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#published_port Service#published_port}
        '''
        result = self._values.get("published_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def publish_mode(self) -> typing.Optional[builtins.str]:
        '''Represents the mode in which the port is to be published: 'ingress' or 'host'. Defaults to ``ingress``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#publish_mode Service#publish_mode}
        '''
        result = self._values.get("publish_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEndpointSpecPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEndpointSpecPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceEndpointSpecPortsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2dbda225b8b63fa7166892710b592b434a26ef09b69715d088a8e1cd831d02b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceEndpointSpecPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7d1eeb84b5338fce1ba635af1e2525b52a31f8025f0750ff8e553f985f1e31)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEndpointSpecPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a46bb530ead74f68005059f25522433b6a0242b91d3721a8f69c58e975ed67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238fa67ea7eb58fb0d8408af7d4009c811223b54d5e18b0d8391e29d1b688482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68f2df94ea2e742b8e98911867f651c7254e6f032c02a68f00df4a53cc4c4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4766144094e9457086870b609a5dc0d83069eb066441bd5edc6335dc2fa7b3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEndpointSpecPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceEndpointSpecPortsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28e628e0914a64b8d4423b039f17d932710cfc279b305a9ecc9a1da43824a4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetPublishedPort")
    def reset_published_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishedPort", []))

    @jsii.member(jsii_name="resetPublishMode")
    def reset_publish_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishMode", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="publishedPortInput")
    def published_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "publishedPortInput"))

    @builtins.property
    @jsii.member(jsii_name="publishModeInput")
    def publish_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publishModeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPortInput")
    def target_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetPortInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3160ff41bfbbca1cb0f1b5e591bcddc64ed7e3651014c3be249820f11150ffdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859f9cfcf5efac3350057ec250056df8dda3b5a86cbac49b47a1b0354d136038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishedPort")
    def published_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "publishedPort"))

    @published_port.setter
    def published_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055e18fcca13f3ab071f976ce666db2f6c36c10a1c7735a990039a101928e9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishedPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishMode")
    def publish_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publishMode"))

    @publish_mode.setter
    def publish_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2842bece6867e5534713542ab49d35b359178e05e4c0b4c22fd2cd84bbd6f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPort")
    def target_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetPort"))

    @target_port.setter
    def target_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde9fca8ab5cfa202105881dbe096f46f000d64dfcccce7f9be20c3db10b3c28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadebe95e21ffcaa6c1df3b5272289f8dcefd7365461ee3eddbe88af2c71b5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718759b785ee227441182ba9648060c5cbfa27860f45fab56e125b5f079ae7ba)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceLabelsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1fb3e414d6eb06ebb7782b8895b6c3f44ab7ccda06cd95e757ae944cb9b267)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf1431ee58a338bf3cf967c5f57006c3f933783f86badeeaae48f14d9cc009b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce27a149872579508e8bceaf65123705800e1e38e0f91369ab5babcce500932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f3e5c51c26c8be8c12be1849676d1b99034e97b3c16a6bcaacc00adcc64944)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2d76c1cdba7ac3033394c3df5ea5a888ecc1241ba2af241518237c29469135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c2fcab177c89d8e07be86e88563677b62cac6cace043579c9f88bb74a11d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceLabelsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccac8d4c6c37d738ab2560ff9991a6b606f70380416db1d6992f8e56812501e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3f70d2efe0c9e515447c820cfeee444c9673307fd0a57b73310635a1c2a2f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cf2f9cde60680525e5257ecfd639f8d68b268cd1edecf7847cea52e4184901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d34f01350c32712e24af28798cb35bf21ae5214d00117dbf67fc61732c1d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceMode",
    jsii_struct_bases=[],
    name_mapping={"global_": "global", "replicated": "replicated"},
)
class ServiceMode:
    def __init__(
        self,
        *,
        global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replicated: typing.Optional[typing.Union["ServiceModeReplicated", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param global_: The global service mode. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#global Service#global}
        :param replicated: replicated block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicated Service#replicated}
        '''
        if isinstance(replicated, dict):
            replicated = ServiceModeReplicated(**replicated)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eeee4162ddd2fa6575aa89be006cdd82a912a6ea38a0ad7d7d1a017e6397342)
            check_type(argname="argument global_", value=global_, expected_type=type_hints["global_"])
            check_type(argname="argument replicated", value=replicated, expected_type=type_hints["replicated"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if global_ is not None:
            self._values["global_"] = global_
        if replicated is not None:
            self._values["replicated"] = replicated

    @builtins.property
    def global_(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The global service mode. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#global Service#global}
        '''
        result = self._values.get("global_")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replicated(self) -> typing.Optional["ServiceModeReplicated"]:
        '''replicated block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicated Service#replicated}
        '''
        result = self._values.get("replicated")
        return typing.cast(typing.Optional["ServiceModeReplicated"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceMode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceModeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceModeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce67e25e193bc9fbdd80d504076b5b2a1a8645e2a2260b30790158b09903c750)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putReplicated")
    def put_replicated(self, *, replicas: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param replicas: The amount of replicas of the service. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicas Service#replicas}
        '''
        value = ServiceModeReplicated(replicas=replicas)

        return typing.cast(None, jsii.invoke(self, "putReplicated", [value]))

    @jsii.member(jsii_name="resetGlobal")
    def reset_global(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGlobal", []))

    @jsii.member(jsii_name="resetReplicated")
    def reset_replicated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicated", []))

    @builtins.property
    @jsii.member(jsii_name="replicated")
    def replicated(self) -> "ServiceModeReplicatedOutputReference":
        return typing.cast("ServiceModeReplicatedOutputReference", jsii.get(self, "replicated"))

    @builtins.property
    @jsii.member(jsii_name="globalInput")
    def global_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "globalInput"))

    @builtins.property
    @jsii.member(jsii_name="replicatedInput")
    def replicated_input(self) -> typing.Optional["ServiceModeReplicated"]:
        return typing.cast(typing.Optional["ServiceModeReplicated"], jsii.get(self, "replicatedInput"))

    @builtins.property
    @jsii.member(jsii_name="global")
    def global_(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "global"))

    @global_.setter
    def global_(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__033879d6c821a7e5730bf7e5ee5dd1ca520601f962ebe3f1314afb87e578dbde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "global", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceMode]:
        return typing.cast(typing.Optional[ServiceMode], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceMode]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22db1e02983bc97bd85640043775289f4992827ae059ae7117bd9f15f37aad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceModeReplicated",
    jsii_struct_bases=[],
    name_mapping={"replicas": "replicas"},
)
class ServiceModeReplicated:
    def __init__(self, *, replicas: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param replicas: The amount of replicas of the service. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicas Service#replicas}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9452e65cac37ffac3b0e95cd282e30ef133f31072208ea0997c371acbf8e0ffc)
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        '''The amount of replicas of the service. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#replicas Service#replicas}
        '''
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceModeReplicated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceModeReplicatedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceModeReplicatedOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eb0628d3dae2bc901e5b8eaf66e1909d9ecf8d0dcc6315728df469a9db67df9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReplicas")
    def reset_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicas", []))

    @builtins.property
    @jsii.member(jsii_name="replicasInput")
    def replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "replicasInput"))

    @builtins.property
    @jsii.member(jsii_name="replicas")
    def replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "replicas"))

    @replicas.setter
    def replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd77865a7cf4b122a8f4e9ed0be72898322146603589162814bce1160e063443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceModeReplicated]:
        return typing.cast(typing.Optional[ServiceModeReplicated], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceModeReplicated]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e146850c888f2e84adb0059601447246b59552d72566f5ae8404dfb4dc6dc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceRollbackConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceRollbackConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param failure_action: Action on rollback failure: pause | continue. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during a rollback. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        :param order: Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917bb9735b94339f11f066516eb3c40958edb6e7234c1ddc0de19050c2e6b727)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument failure_action", value=failure_action, expected_type=type_hints["failure_action"])
            check_type(argname="argument max_failure_ratio", value=max_failure_ratio, expected_type=type_hints["max_failure_ratio"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between task rollbacks (ns|us|ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_action(self) -> typing.Optional[builtins.str]:
        '''Action on rollback failure: pause | continue. Defaults to ``pause``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        '''
        result = self._values.get("failure_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[builtins.str]:
        '''Failure rate to tolerate during a rollback. Defaults to ``0.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        '''
        result = self._values.get("max_failure_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''Duration after each task rollback to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Rollback order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of tasks to be rollbacked in one iteration. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceRollbackConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceRollbackConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceRollbackConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0a23196b99beaccdf59baf4ed8230e67e2e89ee86d41c3391d36f3ef1942778)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetFailureAction")
    def reset_failure_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureAction", []))

    @jsii.member(jsii_name="resetMaxFailureRatio")
    def reset_max_failure_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailureRatio", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="failureActionInput")
    def failure_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureActionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatioInput")
    def max_failure_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxFailureRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa00cb763d7ce3c42f0583ffc50fd1d44ea953ae96a7f7ed7dbda4df2b5781f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureAction")
    def failure_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureAction"))

    @failure_action.setter
    def failure_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9b17b3fdf7478a63debab0d0d97ad5d9355052c188960230842cccf10c470c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatio")
    def max_failure_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxFailureRatio"))

    @max_failure_ratio.setter
    def max_failure_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f5539617fe2515c87f3558840aeea9358f7dd78afc47280d756ad7731800d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailureRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @monitor.setter
    def monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f0eb28d1c74e7d6f927ebf33cc1ab812498ad8783c6fc6ad3d7210903bd94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a9e024a1c0d4f547cc6b5a7bac99da3d5de8f4efe67214f93a18aa408ee612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c013353840748671bc4738a24e51b77b0e2fa4fa4d94b4d2bcf677e0ba1f32af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceRollbackConfig]:
        return typing.cast(typing.Optional[ServiceRollbackConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceRollbackConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e372f2faab2138a91e6f66763b1b5a5c7729637a952f67a6fff2dc9c4e99a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpec",
    jsii_struct_bases=[],
    name_mapping={
        "container_spec": "containerSpec",
        "force_update": "forceUpdate",
        "log_driver": "logDriver",
        "networks_advanced": "networksAdvanced",
        "placement": "placement",
        "resources": "resources",
        "restart_policy": "restartPolicy",
        "runtime": "runtime",
    },
)
class ServiceTaskSpec:
    def __init__(
        self,
        *,
        container_spec: typing.Union["ServiceTaskSpecContainerSpec", typing.Dict[builtins.str, typing.Any]],
        force_update: typing.Optional[jsii.Number] = None,
        log_driver: typing.Optional[typing.Union["ServiceTaskSpecLogDriver", typing.Dict[builtins.str, typing.Any]]] = None,
        networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecNetworksAdvanced", typing.Dict[builtins.str, typing.Any]]]]] = None,
        placement: typing.Optional[typing.Union["ServiceTaskSpecPlacement", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["ServiceTaskSpecResources", typing.Dict[builtins.str, typing.Any]]] = None,
        restart_policy: typing.Optional[typing.Union["ServiceTaskSpecRestartPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_spec: container_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#container_spec Service#container_spec}
        :param force_update: A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#force_update Service#force_update}
        :param log_driver: log_driver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#log_driver Service#log_driver}
        :param networks_advanced: networks_advanced block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#networks_advanced Service#networks_advanced}
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#placement Service#placement}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#resources Service#resources}
        :param restart_policy: restart_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#restart_policy Service#restart_policy}
        :param runtime: Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#runtime Service#runtime}
        '''
        if isinstance(container_spec, dict):
            container_spec = ServiceTaskSpecContainerSpec(**container_spec)
        if isinstance(log_driver, dict):
            log_driver = ServiceTaskSpecLogDriver(**log_driver)
        if isinstance(placement, dict):
            placement = ServiceTaskSpecPlacement(**placement)
        if isinstance(resources, dict):
            resources = ServiceTaskSpecResources(**resources)
        if isinstance(restart_policy, dict):
            restart_policy = ServiceTaskSpecRestartPolicy(**restart_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830aa6e15ad5670e9a056cb802a29fb54a52e8b0c9d86ae956de92122be67cfe)
            check_type(argname="argument container_spec", value=container_spec, expected_type=type_hints["container_spec"])
            check_type(argname="argument force_update", value=force_update, expected_type=type_hints["force_update"])
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument networks_advanced", value=networks_advanced, expected_type=type_hints["networks_advanced"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument restart_policy", value=restart_policy, expected_type=type_hints["restart_policy"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_spec": container_spec,
        }
        if force_update is not None:
            self._values["force_update"] = force_update
        if log_driver is not None:
            self._values["log_driver"] = log_driver
        if networks_advanced is not None:
            self._values["networks_advanced"] = networks_advanced
        if placement is not None:
            self._values["placement"] = placement
        if resources is not None:
            self._values["resources"] = resources
        if restart_policy is not None:
            self._values["restart_policy"] = restart_policy
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def container_spec(self) -> "ServiceTaskSpecContainerSpec":
        '''container_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#container_spec Service#container_spec}
        '''
        result = self._values.get("container_spec")
        assert result is not None, "Required property 'container_spec' is missing"
        return typing.cast("ServiceTaskSpecContainerSpec", result)

    @builtins.property
    def force_update(self) -> typing.Optional[jsii.Number]:
        '''A counter that triggers an update even if no relevant parameters have been changed. See the `spec <https://github.com/docker/swarmkit/blob/master/api/specs.proto#L126>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#force_update Service#force_update}
        '''
        result = self._values.get("force_update")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_driver(self) -> typing.Optional["ServiceTaskSpecLogDriver"]:
        '''log_driver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#log_driver Service#log_driver}
        '''
        result = self._values.get("log_driver")
        return typing.cast(typing.Optional["ServiceTaskSpecLogDriver"], result)

    @builtins.property
    def networks_advanced(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecNetworksAdvanced"]]]:
        '''networks_advanced block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#networks_advanced Service#networks_advanced}
        '''
        result = self._values.get("networks_advanced")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecNetworksAdvanced"]]], result)

    @builtins.property
    def placement(self) -> typing.Optional["ServiceTaskSpecPlacement"]:
        '''placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#placement Service#placement}
        '''
        result = self._values.get("placement")
        return typing.cast(typing.Optional["ServiceTaskSpecPlacement"], result)

    @builtins.property
    def resources(self) -> typing.Optional["ServiceTaskSpecResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#resources Service#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["ServiceTaskSpecResources"], result)

    @builtins.property
    def restart_policy(self) -> typing.Optional["ServiceTaskSpecRestartPolicy"]:
        '''restart_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#restart_policy Service#restart_policy}
        '''
        result = self._values.get("restart_policy")
        return typing.cast(typing.Optional["ServiceTaskSpecRestartPolicy"], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''Runtime is the type of runtime specified for the task executor. See the `types <https://github.com/moby/moby/blob/master/api/types/swarm/runtime.go>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#runtime Service#runtime}
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "cap_add": "capAdd",
        "cap_drop": "capDrop",
        "command": "command",
        "configs": "configs",
        "dir": "dir",
        "dns_config": "dnsConfig",
        "env": "env",
        "groups": "groups",
        "healthcheck": "healthcheck",
        "hostname": "hostname",
        "hosts": "hosts",
        "isolation": "isolation",
        "labels": "labels",
        "mounts": "mounts",
        "privileges": "privileges",
        "read_only": "readOnly",
        "secrets": "secrets",
        "stop_grace_period": "stopGracePeriod",
        "stop_signal": "stopSignal",
        "sysctl": "sysctl",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpec:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        cap_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        cap_drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dir: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecDnsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecHealthcheck", typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecHosts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileges: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivileges", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        stop_grace_period: typing.Optional[builtins.str] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#image Service#image}
        :param args: Arguments to the command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#args Service#args}
        :param cap_add: List of Linux capabilities to add to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_add Service#cap_add}
        :param cap_drop: List of Linux capabilities to drop from the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_drop Service#cap_drop}
        :param command: The command/entrypoint to be run in the image. According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#command Service#command}
        :param configs: configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#configs Service#configs}
        :param dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dir Service#dir}
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dns_config Service#dns_config}
        :param env: A list of environment variables in the form VAR="value". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#env Service#env}
        :param groups: A list of additional groups that the container process will run as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#groups Service#groups}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#healthcheck Service#healthcheck}
        :param hostname: The hostname to use for the container, as a valid RFC 1123 hostname. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hostname Service#hostname}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hosts Service#hosts}
        :param isolation: Isolation technology of the containers running the service. (Windows only). Defaults to ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#isolation Service#isolation}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mounts Service#mounts}
        :param privileges: privileges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#privileges Service#privileges}
        :param read_only: Mount the container's root filesystem as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#read_only Service#read_only}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secrets Service#secrets}
        :param stop_grace_period: Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h). If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_grace_period Service#stop_grace_period}
        :param stop_signal: Signal to stop the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_signal Service#stop_signal}
        :param sysctl: Sysctls config (Linux only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#sysctl Service#sysctl}
        :param user: The user inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        if isinstance(dns_config, dict):
            dns_config = ServiceTaskSpecContainerSpecDnsConfig(**dns_config)
        if isinstance(healthcheck, dict):
            healthcheck = ServiceTaskSpecContainerSpecHealthcheck(**healthcheck)
        if isinstance(privileges, dict):
            privileges = ServiceTaskSpecContainerSpecPrivileges(**privileges)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf7797ac5369c042b72ebf4dca7e9cde9c6b303108ce7a022f98010ae9a71a3)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument cap_add", value=cap_add, expected_type=type_hints["cap_add"])
            check_type(argname="argument cap_drop", value=cap_drop, expected_type=type_hints["cap_drop"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument configs", value=configs, expected_type=type_hints["configs"])
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
            check_type(argname="argument dns_config", value=dns_config, expected_type=type_hints["dns_config"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument healthcheck", value=healthcheck, expected_type=type_hints["healthcheck"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument isolation", value=isolation, expected_type=type_hints["isolation"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mounts", value=mounts, expected_type=type_hints["mounts"])
            check_type(argname="argument privileges", value=privileges, expected_type=type_hints["privileges"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument stop_grace_period", value=stop_grace_period, expected_type=type_hints["stop_grace_period"])
            check_type(argname="argument stop_signal", value=stop_signal, expected_type=type_hints["stop_signal"])
            check_type(argname="argument sysctl", value=sysctl, expected_type=type_hints["sysctl"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if cap_add is not None:
            self._values["cap_add"] = cap_add
        if cap_drop is not None:
            self._values["cap_drop"] = cap_drop
        if command is not None:
            self._values["command"] = command
        if configs is not None:
            self._values["configs"] = configs
        if dir is not None:
            self._values["dir"] = dir
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if env is not None:
            self._values["env"] = env
        if groups is not None:
            self._values["groups"] = groups
        if healthcheck is not None:
            self._values["healthcheck"] = healthcheck
        if hostname is not None:
            self._values["hostname"] = hostname
        if hosts is not None:
            self._values["hosts"] = hosts
        if isolation is not None:
            self._values["isolation"] = isolation
        if labels is not None:
            self._values["labels"] = labels
        if mounts is not None:
            self._values["mounts"] = mounts
        if privileges is not None:
            self._values["privileges"] = privileges
        if read_only is not None:
            self._values["read_only"] = read_only
        if secrets is not None:
            self._values["secrets"] = secrets
        if stop_grace_period is not None:
            self._values["stop_grace_period"] = stop_grace_period
        if stop_signal is not None:
            self._values["stop_signal"] = stop_signal
        if sysctl is not None:
            self._values["sysctl"] = sysctl
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def image(self) -> builtins.str:
        '''The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#image Service#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the command.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#args Service#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cap_add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Linux capabilities to add to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_add Service#cap_add}
        '''
        result = self._values.get("cap_add")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cap_drop(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Linux capabilities to drop from the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_drop Service#cap_drop}
        '''
        result = self._values.get("cap_drop")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The command/entrypoint to be run in the image.

        According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#command Service#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecConfigs"]]]:
        '''configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#configs Service#configs}
        '''
        result = self._values.get("configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecConfigs"]]], result)

    @builtins.property
    def dir(self) -> typing.Optional[builtins.str]:
        '''The working directory for commands to run in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dir Service#dir}
        '''
        result = self._values.get("dir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_config(self) -> typing.Optional["ServiceTaskSpecContainerSpecDnsConfig"]:
        '''dns_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dns_config Service#dns_config}
        '''
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecDnsConfig"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A list of environment variables in the form VAR="value".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#env Service#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of additional groups that the container process will run as.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#groups Service#groups}
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def healthcheck(self) -> typing.Optional["ServiceTaskSpecContainerSpecHealthcheck"]:
        '''healthcheck block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#healthcheck Service#healthcheck}
        '''
        result = self._values.get("healthcheck")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecHealthcheck"], result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''The hostname to use for the container, as a valid RFC 1123 hostname.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hostname Service#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hosts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecHosts"]]]:
        '''hosts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hosts Service#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecHosts"]]], result)

    @builtins.property
    def isolation(self) -> typing.Optional[builtins.str]:
        '''Isolation technology of the containers running the service. (Windows only). Defaults to ``default``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#isolation Service#isolation}
        '''
        result = self._values.get("isolation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecLabels"]]], result)

    @builtins.property
    def mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMounts"]]]:
        '''mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mounts Service#mounts}
        '''
        result = self._values.get("mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMounts"]]], result)

    @builtins.property
    def privileges(self) -> typing.Optional["ServiceTaskSpecContainerSpecPrivileges"]:
        '''privileges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#privileges Service#privileges}
        '''
        result = self._values.get("privileges")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivileges"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Mount the container's root filesystem as read only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#read_only Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secrets Service#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]], result)

    @builtins.property
    def stop_grace_period(self) -> typing.Optional[builtins.str]:
        '''Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h).

        If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_grace_period Service#stop_grace_period}
        '''
        result = self._values.get("stop_grace_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stop_signal(self) -> typing.Optional[builtins.str]:
        '''Signal to stop the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_signal Service#stop_signal}
        '''
        result = self._values.get("stop_signal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sysctl(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sysctls config (Linux only).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#sysctl Service#sysctl}
        '''
        result = self._values.get("sysctl")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''The user inside the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "config_id": "configId",
        "file_name": "fileName",
        "config_name": "configName",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
    },
)
class ServiceTaskSpecContainerSpecConfigs:
    def __init__(
        self,
        *,
        config_id: builtins.str,
        file_name: builtins.str,
        config_name: typing.Optional[builtins.str] = None,
        file_gid: typing.Optional[builtins.str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_id: ID of the specific config that we're referencing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#config_id Service#config_id}
        :param file_name: Represents the final filename in the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_name Service#file_name}
        :param config_name: Name of the config that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#config_name Service#config_name}
        :param file_gid: Represents the file GID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_gid Service#file_gid}
        :param file_mode: Represents represents the FileMode of the file. Defaults to ``0o444``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_mode Service#file_mode}
        :param file_uid: Represents the file UID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_uid Service#file_uid}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d249dec05b44127fdc5898520f1e89582ced475cc99b3189caed2653f1d415)
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument config_name", value=config_name, expected_type=type_hints["config_name"])
            check_type(argname="argument file_gid", value=file_gid, expected_type=type_hints["file_gid"])
            check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
            check_type(argname="argument file_uid", value=file_uid, expected_type=type_hints["file_uid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_id": config_id,
            "file_name": file_name,
        }
        if config_name is not None:
            self._values["config_name"] = config_name
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid

    @builtins.property
    def config_id(self) -> builtins.str:
        '''ID of the specific config that we're referencing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#config_id Service#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_name(self) -> builtins.str:
        '''Represents the final filename in the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_name Service#file_name}
        '''
        result = self._values.get("file_name")
        assert result is not None, "Required property 'file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config_name(self) -> typing.Optional[builtins.str]:
        '''Name of the config that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#config_name Service#config_name}
        '''
        result = self._values.get("config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_gid(self) -> typing.Optional[builtins.str]:
        '''Represents the file GID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_gid Service#file_gid}
        '''
        result = self._values.get("file_gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        '''Represents represents the FileMode of the file. Defaults to ``0o444``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_mode Service#file_mode}
        '''
        result = self._values.get("file_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_uid(self) -> typing.Optional[builtins.str]:
        '''Represents the file UID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_uid Service#file_uid}
        '''
        result = self._values.get("file_uid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecConfigsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fbccc2c7f1e0b6d648ab69f0bd3436a4b416e45f59c7fce17a9327e02d4b88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe2638a4deb83fe4f0ef18ec58139815df573ba2abea9d65c299af6c9aa2cec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d876f5888266d862f575c1b392a051288a933b8d992f26432dd267025ed35d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590513d2abeae251f65f030cf307a219cc0940d7e0a9f8bd0e03b6b133e762c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a385e8a437ed7b65dd439514349a8e67eb80b11ee4d6dec1eb1c6154905345d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca76f68f95913963c095b42ab390f1d9b448bd4686fea6b0ea9997016d6c5b3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecConfigsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af8d8c6405785132cb5328173f4472d0b1e1eeac50381a31b5722fb6a662a83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfigName")
    def reset_config_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigName", []))

    @jsii.member(jsii_name="resetFileGid")
    def reset_file_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileGid", []))

    @jsii.member(jsii_name="resetFileMode")
    def reset_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMode", []))

    @jsii.member(jsii_name="resetFileUid")
    def reset_file_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUid", []))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configNameInput")
    def config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileGidInput")
    def file_gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileGidInput"))

    @builtins.property
    @jsii.member(jsii_name="fileModeInput")
    def file_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUidInput")
    def file_uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileUidInput"))

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fcf82a0ad78cd7e76089c467129fdc0ee2060143eeb67dc1475c4f2bf9dbf42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configName")
    def config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configName"))

    @config_name.setter
    def config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11e413f7dcbac71cd0492880cb01c009022e4273335fde32a573f1ee9563855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileGid")
    def file_gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileGid"))

    @file_gid.setter
    def file_gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df74318797136516130074c12b0d5f83217164a7e8574e3178b9697c91a35bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileMode")
    def file_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileMode"))

    @file_mode.setter
    def file_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d56bac005cb988cae3da456c7274c8de61f53e4eeabd3a2e9a77766328d6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88e83b3285fce1a66e912c25e0eda563694726a3feb498ef33dad43fe21f0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUid")
    def file_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileUid"))

    @file_uid.setter
    def file_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ad721fb2d71fe591293533b366af39b10e09763d914bb2db91aef6d6a55ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765d9d758d63decc4b8e5785639e9dafef498efdb5413e15fc352e6f783412ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecDnsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "nameservers": "nameservers",
        "options": "options",
        "search": "search",
    },
)
class ServiceTaskSpecContainerSpecDnsConfig:
    def __init__(
        self,
        *,
        nameservers: typing.Sequence[builtins.str],
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        search: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param nameservers: The IP addresses of the name servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nameservers Service#nameservers}
        :param options: A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        :param search: A search list for host-name lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#search Service#search}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9abf56519b143da582c8f4c1019073b156be13dd67beaea1e5b9cfdf33288e)
            check_type(argname="argument nameservers", value=nameservers, expected_type=type_hints["nameservers"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "nameservers": nameservers,
        }
        if options is not None:
            self._values["options"] = options
        if search is not None:
            self._values["search"] = search

    @builtins.property
    def nameservers(self) -> typing.List[builtins.str]:
        '''The IP addresses of the name servers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nameservers Service#nameservers}
        '''
        result = self._values.get("nameservers")
        assert result is not None, "Required property 'nameservers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A search list for host-name lookup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#search Service#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecDnsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecDnsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecDnsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90b69de7bcf419b852f914f04a56fdc71194b43e12013b35a8e54bcf302c3a4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @builtins.property
    @jsii.member(jsii_name="nameserversInput")
    def nameservers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nameserversInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameservers")
    def nameservers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nameservers"))

    @nameservers.setter
    def nameservers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160710e15c898783dbae2a558ab4482704bb50aed0f4bc665066bdaa99b35c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameservers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aed0e1de60d7e5fadd28bd1ef474f3f5d06a010eebd282de09e04a0bb9246c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "search"))

    @search.setter
    def search(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__647ca625180d9c17aaf9c6b6ceb8124f6f19ec126fde358cd69bd5a0d5c17066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "search", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpecDnsConfig]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecDnsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecDnsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a80c1127eece90366f6e360b01bc79a3ea7d9df3ee4a3ccdafce99d495941b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecHealthcheck",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "interval": "interval",
        "retries": "retries",
        "start_period": "startPeriod",
        "timeout": "timeout",
    },
)
class ServiceTaskSpecContainerSpecHealthcheck:
    def __init__(
        self,
        *,
        test: typing.Sequence[builtins.str],
        interval: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param test: The test to perform as list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#test Service#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#interval Service#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#retries Service#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#start_period Service#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc05914071b7efa59cac5489c0ac4dd26e0a3efa5943fc0cbc1692bacdecd3f)
            check_type(argname="argument test", value=test, expected_type=type_hints["test"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument start_period", value=start_period, expected_type=type_hints["start_period"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "test": test,
        }
        if interval is not None:
            self._values["interval"] = interval
        if retries is not None:
            self._values["retries"] = retries
        if start_period is not None:
            self._values["start_period"] = start_period
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def test(self) -> typing.List[builtins.str]:
        '''The test to perform as list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#test Service#test}
        '''
        result = self._values.get("test")
        assert result is not None, "Required property 'test' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Time between running the check (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#interval Service#interval}
        '''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''Consecutive failures needed to report unhealthy. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#retries Service#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_period(self) -> typing.Optional[builtins.str]:
        '''Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#start_period Service#start_period}
        '''
        result = self._values.get("start_period")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHealthcheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecHealthcheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecHealthcheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfb3ad99b5425671cf8428179d370f1b173bd98afeaecc8025a470654b901d18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="resetRetries")
    def reset_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetries", []))

    @jsii.member(jsii_name="resetStartPeriod")
    def reset_start_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartPeriod", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="startPeriodInput")
    def start_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="testInput")
    def test_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "testInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868d2d536a14b4ed24bca8f976c1a8bcea10f12dde3f61714e817dc6914c3ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d28590fb82cc52dee8c6b2f35e92f6c3ead92bd30183b49de711e357e4aa1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startPeriod")
    def start_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startPeriod"))

    @start_period.setter
    def start_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389295cd1df74a6c154f4b2c69b3ce00e8402463117443bc50dbe660336fcf1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="test")
    def test(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "test"))

    @test.setter
    def test(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6150461fada1c8deaed1a94c4a7dd12046ad706c2c8705cc9d606e7127ea4f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "test", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e7030bbb48cb8fa58f0ee2e26dad0ce2f67708fe13dbcb6e11ad4f611188fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecHealthcheck]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecHealthcheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecHealthcheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81e740fff23d35c391a241a9901573df43c9d0a0f59c215f598d8bb7589d953c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecHosts",
    jsii_struct_bases=[],
    name_mapping={"host": "host", "ip": "ip"},
)
class ServiceTaskSpecContainerSpecHosts:
    def __init__(self, *, host: builtins.str, ip: builtins.str) -> None:
        '''
        :param host: The name of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#host Service#host}
        :param ip: The ip of the host. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#ip Service#ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bf1ec40a4ee60f8f8a74ab412827c3cfbc7421c9221619f4993f53fb0e83d1)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "ip": ip,
        }

    @builtins.property
    def host(self) -> builtins.str:
        '''The name of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#host Service#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip(self) -> builtins.str:
        '''The ip of the host.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#ip Service#ip}
        '''
        result = self._values.get("ip")
        assert result is not None, "Required property 'ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecHosts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecHostsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecHostsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbfc4daf99d95aa1fba30bd22812241677bff087b968ee7632b09f55088d3cd4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecHostsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb47e7f3046a9f186e0e1b260bb156c8c8106fd1aeaca64ef5cf6f6730d8011)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecHostsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9a9fba1de8f26e8b63aa74060ee8fbe840ca647769f601029cc25ab70eac7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e1ee69d0d93c3934e0ab8de8c490f6cc9c74d98934c6dda77c65c691edf401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c14e1ce4606a4a98df5130c70bab695445e7ea6ede527d054555cf674a56a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc69681e20a855d3d3e888dbb4ba3aed082ea8ef6e59c76a89698140f85b7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecHostsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecHostsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75c8b8814ed8bf8e50f6041441462168285cc714e8d8804b70a40b547237c99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fa596ded4e77b84e395d1058b112371714331c525f65eb1b71c7766520b141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b05553424f2e05f554d9fc80b6e45487822d197b897dce1ad41a67c0efe783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c5b293f720d943a5e2c12442fcb5a4ee590324f0c10d57ba9c56e8b50ee93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14636036c1dbc368581cfabb5969ca56f7ceb24a3832a12ea056e5870327b089)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecLabelsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7feecb6ba6cc9411f30ead2387ebc022d2abf0d8858dc522ba035546058c2907)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a470f69d5fee6ca660e1c0348ff8a4cef2841381eb7dc18248640af9a6c717ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc16981802bc4da75ea8ef089d79fe387a71e9be1f076ec4dd87959523f9e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246d2bf65facc0014ae0e157c8e2e260b62c5c58ded233bf548df82e693b2b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a07ff2d459cb0a8440949877a7575e98e7909c3d352b6c3b612c728f398ecb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb8004a8f0422052bf9e7e60abf079cc7f599a10b389867212db6a92f958c54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecLabelsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15a3f5198962dd4fb0a657b9fc28b56ce17c3cf29eb64b98186bd79bbc6b7b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e87045f1ff7789c556bcf3b3a82cad1aa39e6b2a7323108c9a782060d70782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bba8fef9fad1facefcd241682e6e70b684a0c4546e3159aba01ef32aba8e0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63344f3b810ffa96d47a7ae653943725a4a18e8a265f50cd61c7f4c76156a023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMounts",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "type": "type",
        "bind_options": "bindOptions",
        "read_only": "readOnly",
        "source": "source",
        "tmpfs_options": "tmpfsOptions",
        "volume_options": "volumeOptions",
    },
)
class ServiceTaskSpecContainerSpecMounts:
    def __init__(
        self,
        *,
        target: builtins.str,
        type: builtins.str,
        bind_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsBindOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        source: typing.Optional[builtins.str] = None,
        tmpfs_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsTmpfsOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_options: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param target: Container path. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#target Service#target}
        :param type: The mount type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#type Service#type}
        :param bind_options: bind_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#bind_options Service#bind_options}
        :param read_only: Whether the mount should be read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#read_only Service#read_only}
        :param source: Mount source (e.g. a volume name, a host path). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#source Service#source}
        :param tmpfs_options: tmpfs_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#tmpfs_options Service#tmpfs_options}
        :param volume_options: volume_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#volume_options Service#volume_options}
        '''
        if isinstance(bind_options, dict):
            bind_options = ServiceTaskSpecContainerSpecMountsBindOptions(**bind_options)
        if isinstance(tmpfs_options, dict):
            tmpfs_options = ServiceTaskSpecContainerSpecMountsTmpfsOptions(**tmpfs_options)
        if isinstance(volume_options, dict):
            volume_options = ServiceTaskSpecContainerSpecMountsVolumeOptions(**volume_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e5b5738704c296c7808449c3a58dcd2b5bbaa8ef544378487e4f7f65944671)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument bind_options", value=bind_options, expected_type=type_hints["bind_options"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tmpfs_options", value=tmpfs_options, expected_type=type_hints["tmpfs_options"])
            check_type(argname="argument volume_options", value=volume_options, expected_type=type_hints["volume_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "type": type,
        }
        if bind_options is not None:
            self._values["bind_options"] = bind_options
        if read_only is not None:
            self._values["read_only"] = read_only
        if source is not None:
            self._values["source"] = source
        if tmpfs_options is not None:
            self._values["tmpfs_options"] = tmpfs_options
        if volume_options is not None:
            self._values["volume_options"] = volume_options

    @builtins.property
    def target(self) -> builtins.str:
        '''Container path.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#target Service#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The mount type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#type Service#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bind_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsBindOptions"]:
        '''bind_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#bind_options Service#bind_options}
        '''
        result = self._values.get("bind_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsBindOptions"], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the mount should be read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#read_only Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Mount source (e.g. a volume name, a host path).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#source Service#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tmpfs_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]:
        '''tmpfs_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#tmpfs_options Service#tmpfs_options}
        '''
        result = self._values.get("tmpfs_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"], result)

    @builtins.property
    def volume_options(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"]:
        '''volume_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#volume_options Service#volume_options}
        '''
        result = self._values.get("volume_options")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsBindOptions",
    jsii_struct_bases=[],
    name_mapping={"propagation": "propagation"},
)
class ServiceTaskSpecContainerSpecMountsBindOptions:
    def __init__(self, *, propagation: typing.Optional[builtins.str] = None) -> None:
        '''
        :param propagation: Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount. See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#propagation Service#propagation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2484428e63894de3c13d4e21fc7e6462da0b323465e42cd7a69205daf6864cbd)
            check_type(argname="argument propagation", value=propagation, expected_type=type_hints["propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if propagation is not None:
            self._values["propagation"] = propagation

    @builtins.property
    def propagation(self) -> typing.Optional[builtins.str]:
        '''Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount.

        See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#propagation Service#propagation}
        '''
        result = self._values.get("propagation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51dd3e5a6159fdf9d80f1c7fc174192a5f63989b1c37c556a92ddd7878c6d2a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPropagation")
    def reset_propagation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagation", []))

    @builtins.property
    @jsii.member(jsii_name="propagationInput")
    def propagation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "propagationInput"))

    @builtins.property
    @jsii.member(jsii_name="propagation")
    def propagation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "propagation"))

    @propagation.setter
    def propagation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8165fb0c07b85b48653a7931c60284adf7077fb808ec629ff84f683b5eb21b0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8008e0cde8bb77fb27598b384bb9cde4e78649da17ee05c726ca1f8ca3679d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0392030cf0234a8cb380bf292ebd0b475d71637269e95fb552d4ada3492b405e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59aa9f7e9ec12d1c2119c3f594f852d7d7521ebd7723f6e2d96bd452d48a63d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74cbed61f07f28ca6281f04325f1946b1f78bb99fef81a192066053991498e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54685e714bccc9a5ad327943e3322ff5b372ba23f70c1b271bfec954ac0150eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caac5a69b8c51194ac1c22b80e850f8334d6a4b7540646bab05b7288e618cea9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bafb2c8bff1e1730e76f97719c27654cfecdf5d302ea6442705a6afe5aae70dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0958bd29798efe9e9748050b779c08b85440c3e17416307255478a95a5cd9c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBindOptions")
    def put_bind_options(
        self,
        *,
        propagation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param propagation: Bind propagation refers to whether or not mounts created within a given bind-mount or named volume can be propagated to replicas of that mount. See the `docs <https://docs.docker.com/storage/bind-mounts/#configure-bind-propagation>`_ for details. Defaults to ``rprivate`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#propagation Service#propagation}
        '''
        value = ServiceTaskSpecContainerSpecMountsBindOptions(propagation=propagation)

        return typing.cast(None, jsii.invoke(self, "putBindOptions", [value]))

    @jsii.member(jsii_name="putTmpfsOptions")
    def put_tmpfs_options(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#size_bytes Service#size_bytes}
        '''
        value = ServiceTaskSpecContainerSpecMountsTmpfsOptions(
            mode=mode, size_bytes=size_bytes
        )

        return typing.cast(None, jsii.invoke(self, "putTmpfsOptions", [value]))

    @jsii.member(jsii_name="putVolumeOptions")
    def put_volume_options(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_name Service#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_options Service#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#no_copy Service#no_copy}
        '''
        value = ServiceTaskSpecContainerSpecMountsVolumeOptions(
            driver_name=driver_name,
            driver_options=driver_options,
            labels=labels,
            no_copy=no_copy,
        )

        return typing.cast(None, jsii.invoke(self, "putVolumeOptions", [value]))

    @jsii.member(jsii_name="resetBindOptions")
    def reset_bind_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBindOptions", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTmpfsOptions")
    def reset_tmpfs_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTmpfsOptions", []))

    @jsii.member(jsii_name="resetVolumeOptions")
    def reset_volume_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeOptions", []))

    @builtins.property
    @jsii.member(jsii_name="bindOptions")
    def bind_options(
        self,
    ) -> ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference, jsii.get(self, "bindOptions"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsOptions")
    def tmpfs_options(
        self,
    ) -> "ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference", jsii.get(self, "tmpfsOptions"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptions")
    def volume_options(
        self,
    ) -> "ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference", jsii.get(self, "volumeOptions"))

    @builtins.property
    @jsii.member(jsii_name="bindOptionsInput")
    def bind_options_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions], jsii.get(self, "bindOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="tmpfsOptionsInput")
    def tmpfs_options_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsTmpfsOptions"], jsii.get(self, "tmpfsOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeOptionsInput")
    def volume_options_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecMountsVolumeOptions"], jsii.get(self, "volumeOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb4f5d2ccbe0ad1149717af6804bfe5077523f7ac66b8ba19a9ea4ec6e6e1cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43566ab5664f9386258b5f28940817fb5bc32789a5ace61ecd7241e5f7ae6f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2069121e9d1c68c9bc7ebf4cb8ba1b7aa61029b3a0c173710e360dc47b3ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119434017910afab9b9095c050ad8ea9db4b9be75a36c48378993b55cf95df26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e4481c160c8e129ae0daa8ea41207a6a7ea7615687d726af3a4f47199e46c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "size_bytes": "sizeBytes"},
)
class ServiceTaskSpecContainerSpecMountsTmpfsOptions:
    def __init__(
        self,
        *,
        mode: typing.Optional[jsii.Number] = None,
        size_bytes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: The permission mode for the tmpfs mount in an integer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        :param size_bytes: The size for the tmpfs mount in bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#size_bytes Service#size_bytes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e289b5c69fe84ef21048faa4e2d3cd2631260cde5f3c26f59895fd88bfe643a)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument size_bytes", value=size_bytes, expected_type=type_hints["size_bytes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mode is not None:
            self._values["mode"] = mode
        if size_bytes is not None:
            self._values["size_bytes"] = size_bytes

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''The permission mode for the tmpfs mount in an integer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mode Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def size_bytes(self) -> typing.Optional[jsii.Number]:
        '''The size for the tmpfs mount in bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#size_bytes Service#size_bytes}
        '''
        result = self._values.get("size_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsTmpfsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d65d355ec0ada2d8003c92bb2b29dd6ff3914f921a56fdcb7ec0c20150833e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetSizeBytes")
    def reset_size_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeBytes", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeBytesInput")
    def size_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2532a415038a208c9640ac612ff93130d1c0f8148caaee46e1bf4d04c3c99e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeBytes")
    def size_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sizeBytes"))

    @size_bytes.setter
    def size_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf38eae48913f49fc5aab6f94d34d818c5e95f204a390cdb6d99ef586c41b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ebb98e76b0b0985a4e75f78154f83088a62598d1b69acf6e38193b93a4ce26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "driver_name": "driverName",
        "driver_options": "driverOptions",
        "labels": "labels",
        "no_copy": "noCopy",
    },
)
class ServiceTaskSpecContainerSpecMountsVolumeOptions:
    def __init__(
        self,
        *,
        driver_name: typing.Optional[builtins.str] = None,
        driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param driver_name: Name of the driver to use to create the volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_name Service#driver_name}
        :param driver_options: key/value map of driver specific options. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_options Service#driver_options}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param no_copy: Populate volume with data from the target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#no_copy Service#no_copy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af05a0939e31cb583eda3d82f21bbb8180d71ca426281ed5a0c1f2394a327cc)
            check_type(argname="argument driver_name", value=driver_name, expected_type=type_hints["driver_name"])
            check_type(argname="argument driver_options", value=driver_options, expected_type=type_hints["driver_options"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument no_copy", value=no_copy, expected_type=type_hints["no_copy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if driver_name is not None:
            self._values["driver_name"] = driver_name
        if driver_options is not None:
            self._values["driver_options"] = driver_options
        if labels is not None:
            self._values["labels"] = labels
        if no_copy is not None:
            self._values["no_copy"] = no_copy

    @builtins.property
    def driver_name(self) -> typing.Optional[builtins.str]:
        '''Name of the driver to use to create the volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_name Service#driver_name}
        '''
        result = self._values.get("driver_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''key/value map of driver specific options.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_options Service#driver_options}
        '''
        result = self._values.get("driver_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels"]]], result)

    @builtins.property
    def no_copy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Populate volume with data from the target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#no_copy Service#no_copy}
        '''
        result = self._values.get("no_copy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    jsii_struct_bases=[],
    name_mapping={"label": "label", "value": "value"},
)
class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels:
    def __init__(self, *, label: builtins.str, value: builtins.str) -> None:
        '''
        :param label: Name of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        :param value: Value of the label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aae8df9f9ae986a5621822664a3fb2b5b9dea2a3f60afce5d44bb55017d447)
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label": label,
            "value": value,
        }

    @builtins.property
    def label(self) -> builtins.str:
        '''Name of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#label Service#label}
        '''
        result = self._values.get("label")
        assert result is not None, "Required property 'label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Value of the label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#value Service#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75081e5335b1dd9365c8b3963bcf061a3ae446d5d0f333be74668ee70d5ef0a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a08c8b3ca5df8f8e8fd8eecabc4d9c74fff9ad3ddb4d0aeb53a07846f338e4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f9677c94739f9acb2d8ff2d5ac6ae4a27f64f9945a5a41d231ac6161f9a176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60cb9bb3024b1f2cb67c24207376209f93f6e43ab233a00da01bd5941a77adec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8446875f6a6a339814a54fa6ab05fb61af92bb07c4a8fb35ccd177229615724b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f11a25a0a8ff43b53a25268297d6eec0fd20f131fc8de5b99583b78a703e1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26a12c601dd7560a45f82ca26ee5a2b0d7f58b2ab82ab7865f49db1f946c95d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a152fc24331f120bf430ce4a06b6b82988e1a7fd1b43b66d561657655055bfd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b0d496b0504bf38af7bfb9a374a904530e81f42662b5ac64841e0555421032)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb6259472aaa0d227bfeb0e2a7f482b1b1d07dfc29a54df4dbb596f312f192c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b911694987bf3755f29ae31e01fcc8e5fe24f4a67111a3867919a7e993637fcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85a4593f586424c70f632746476ba22475c97a4fe424ba059fd52e44ca633f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="resetDriverName")
    def reset_driver_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverName", []))

    @jsii.member(jsii_name="resetDriverOptions")
    def reset_driver_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverOptions", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNoCopy")
    def reset_no_copy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoCopy", []))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList:
        return typing.cast(ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="driverNameInput")
    def driver_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "driverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="driverOptionsInput")
    def driver_options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="noCopyInput")
    def no_copy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noCopyInput"))

    @builtins.property
    @jsii.member(jsii_name="driverName")
    def driver_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverName"))

    @driver_name.setter
    def driver_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68c7f62a60d9eaeb01bf468d0bbe3eae37820856fc6de80e4ea32e0327f163e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOptions")
    def driver_options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverOptions"))

    @driver_options.setter
    def driver_options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9dd1a88f0b1f83e57b8f5b89af694388929bbae4973821b3301eca1036310f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noCopy")
    def no_copy(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noCopy"))

    @no_copy.setter
    def no_copy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e6136dab20d51f2eda610110bf14a8227e5e7c79489f13f0f682fb6a174dde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noCopy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf593e6cc7a673ce1dd22c7674af2f848b3e2f8b308c6bb2ad69800656152763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f9182e35bd3c9badfbf82026615cc795b19604272986f7f66e2ef0aa74c4c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfigs")
    def put_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe32be4ea42618910ff747465a8c777d9225c75d2c8b5d1c3a16d01d22cd10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfigs", [value]))

    @jsii.member(jsii_name="putDnsConfig")
    def put_dns_config(
        self,
        *,
        nameservers: typing.Sequence[builtins.str],
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        search: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param nameservers: The IP addresses of the name servers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nameservers Service#nameservers}
        :param options: A list of internal resolver variables to be modified (e.g., ``debug``, ``ndots:3``, etc.). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        :param search: A search list for host-name lookup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#search Service#search}
        '''
        value = ServiceTaskSpecContainerSpecDnsConfig(
            nameservers=nameservers, options=options, search=search
        )

        return typing.cast(None, jsii.invoke(self, "putDnsConfig", [value]))

    @jsii.member(jsii_name="putHealthcheck")
    def put_healthcheck(
        self,
        *,
        test: typing.Sequence[builtins.str],
        interval: typing.Optional[builtins.str] = None,
        retries: typing.Optional[jsii.Number] = None,
        start_period: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param test: The test to perform as list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#test Service#test}
        :param interval: Time between running the check (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#interval Service#interval}
        :param retries: Consecutive failures needed to report unhealthy. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#retries Service#retries}
        :param start_period: Start period for the container to initialize before counting retries towards unstable (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#start_period Service#start_period}
        :param timeout: Maximum time to allow one check to run (ms|s|m|h). Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#timeout Service#timeout}
        '''
        value = ServiceTaskSpecContainerSpecHealthcheck(
            test=test,
            interval=interval,
            retries=retries,
            start_period=start_period,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthcheck", [value]))

    @jsii.member(jsii_name="putHosts")
    def put_hosts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093bf7c0e614ecfc83df6a4f5c6dfee5bf4971745d6c299660f1f49d562fc49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHosts", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c144e3e27dbe34e2fa6ee57a9180e1b3b84cdf4acaf4b7f5e3d6929e257597b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putMounts")
    def put_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eaa0619e216c0a5a960f685523d044dd87805566ac4e545d91a586cb83fa218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMounts", [value]))

    @jsii.member(jsii_name="putPrivileges")
    def put_privileges(
        self,
        *,
        credential_spec: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux_context: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_spec: credential_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#credential_spec Service#credential_spec}
        :param se_linux_context: se_linux_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        value = ServiceTaskSpecContainerSpecPrivileges(
            credential_spec=credential_spec, se_linux_context=se_linux_context
        )

        return typing.cast(None, jsii.invoke(self, "putPrivileges", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecContainerSpecSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ab23565463b427f6e3c44bd0b6b4cd4ab627e78404dd6efd050dc6e022511b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecrets", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCapAdd")
    def reset_cap_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapAdd", []))

    @jsii.member(jsii_name="resetCapDrop")
    def reset_cap_drop(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapDrop", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetConfigs")
    def reset_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigs", []))

    @jsii.member(jsii_name="resetDir")
    def reset_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDir", []))

    @jsii.member(jsii_name="resetDnsConfig")
    def reset_dns_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsConfig", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetGroups")
    def reset_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroups", []))

    @jsii.member(jsii_name="resetHealthcheck")
    def reset_healthcheck(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthcheck", []))

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetIsolation")
    def reset_isolation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsolation", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMounts")
    def reset_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMounts", []))

    @jsii.member(jsii_name="resetPrivileges")
    def reset_privileges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivileges", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @jsii.member(jsii_name="resetSecrets")
    def reset_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecrets", []))

    @jsii.member(jsii_name="resetStopGracePeriod")
    def reset_stop_grace_period(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopGracePeriod", []))

    @jsii.member(jsii_name="resetStopSignal")
    def reset_stop_signal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStopSignal", []))

    @jsii.member(jsii_name="resetSysctl")
    def reset_sysctl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSysctl", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="configs")
    def configs(self) -> ServiceTaskSpecContainerSpecConfigsList:
        return typing.cast(ServiceTaskSpecContainerSpecConfigsList, jsii.get(self, "configs"))

    @builtins.property
    @jsii.member(jsii_name="dnsConfig")
    def dns_config(self) -> ServiceTaskSpecContainerSpecDnsConfigOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecDnsConfigOutputReference, jsii.get(self, "dnsConfig"))

    @builtins.property
    @jsii.member(jsii_name="healthcheck")
    def healthcheck(self) -> ServiceTaskSpecContainerSpecHealthcheckOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecHealthcheckOutputReference, jsii.get(self, "healthcheck"))

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> ServiceTaskSpecContainerSpecHostsList:
        return typing.cast(ServiceTaskSpecContainerSpecHostsList, jsii.get(self, "hosts"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> ServiceTaskSpecContainerSpecLabelsList:
        return typing.cast(ServiceTaskSpecContainerSpecLabelsList, jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mounts")
    def mounts(self) -> ServiceTaskSpecContainerSpecMountsList:
        return typing.cast(ServiceTaskSpecContainerSpecMountsList, jsii.get(self, "mounts"))

    @builtins.property
    @jsii.member(jsii_name="privileges")
    def privileges(self) -> "ServiceTaskSpecContainerSpecPrivilegesOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecPrivilegesOutputReference", jsii.get(self, "privileges"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "ServiceTaskSpecContainerSpecSecretsList":
        return typing.cast("ServiceTaskSpecContainerSpecSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="capAddInput")
    def cap_add_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capAddInput"))

    @builtins.property
    @jsii.member(jsii_name="capDropInput")
    def cap_drop_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capDropInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="configsInput")
    def configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]], jsii.get(self, "configsInput"))

    @builtins.property
    @jsii.member(jsii_name="dirInput")
    def dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dirInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsConfigInput")
    def dns_config_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecDnsConfig]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecDnsConfig], jsii.get(self, "dnsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="groupsInput")
    def groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupsInput"))

    @builtins.property
    @jsii.member(jsii_name="healthcheckInput")
    def healthcheck_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecHealthcheck]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecHealthcheck], jsii.get(self, "healthcheckInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="isolationInput")
    def isolation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isolationInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="mountsInput")
    def mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]], jsii.get(self, "mountsInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegesInput")
    def privileges_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivileges"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivileges"], jsii.get(self, "privilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsInput")
    def secrets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecContainerSpecSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="stopGracePeriodInput")
    def stop_grace_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stopGracePeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="stopSignalInput")
    def stop_signal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stopSignalInput"))

    @builtins.property
    @jsii.member(jsii_name="sysctlInput")
    def sysctl_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "sysctlInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0d0e2ddfef0221c298bc9fe41f6045a46d8e23b5419ec7bf97a3646d269001)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capAdd")
    def cap_add(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capAdd"))

    @cap_add.setter
    def cap_add(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7721b78fa9f7afc3125d860238ad2ce84651f22821b6676cca9e191dfc16e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capAdd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="capDrop")
    def cap_drop(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capDrop"))

    @cap_drop.setter
    def cap_drop(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ead9d1c511fd77e747b7db69569f9e41e4848741782ee81ff52df2a32ef171f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capDrop", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb467d2da758c7805f59f6f0ba263404054286319f85c537827bd57a96a5755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dir")
    def dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dir"))

    @dir.setter
    def dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0b134416a24f542deef96ae47b50fe2b43ef67c898668977ae0658244b3679)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @env.setter
    def env(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcac20ba0d2887683faa3ca7e10de92623cf5394d7b456ba4ae174be383b5675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7734205260dd74d23fee5152abafc9b36182531d600d0b598154f6453042d7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8c535cee67a662fea3dcf98056c4b9af400d456d0253919b366abf6485365b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe679b10020a7b55fc5ae722d748c1fd6d435dbbfc0cced01cce188699bbf99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isolation")
    def isolation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isolation"))

    @isolation.setter
    def isolation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3956831207ea96c857c976062daabd2f5da85bdbbe9ae115f26034de0c2471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isolation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf0761ab1fb5115bdffe821513258858f43c75dd119cca25f9f6aa4e5530e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopGracePeriod")
    def stop_grace_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stopGracePeriod"))

    @stop_grace_period.setter
    def stop_grace_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e9bff20a6fc7c32f4547c90197d03ec794c50257f636b35dcfa9d724b0c0dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopGracePeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stopSignal")
    def stop_signal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stopSignal"))

    @stop_signal.setter
    def stop_signal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e42dd8705d80516d52239e5bd5d2245867406818cb4b66c899de5a37c57d7bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopSignal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sysctl")
    def sysctl(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "sysctl"))

    @sysctl.setter
    def sysctl(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512fd116e19432efb168a6081504e57386a7d8bc58a38f1dd4f2d878cb88a0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sysctl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f2ec641c8c2509957a126b12034e6156a5c507856e329be557a84d1a6a12af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c9e37912f628014316e53bdb6100003b3a8b006a3b12dd320d48a312749bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivileges",
    jsii_struct_bases=[],
    name_mapping={
        "credential_spec": "credentialSpec",
        "se_linux_context": "seLinuxContext",
    },
)
class ServiceTaskSpecContainerSpecPrivileges:
    def __init__(
        self,
        *,
        credential_spec: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        se_linux_context: typing.Optional[typing.Union["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param credential_spec: credential_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#credential_spec Service#credential_spec}
        :param se_linux_context: se_linux_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        if isinstance(credential_spec, dict):
            credential_spec = ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(**credential_spec)
        if isinstance(se_linux_context, dict):
            se_linux_context = ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(**se_linux_context)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae949591f45fd69600eebc18b2bdfa82f7afc10d75a11fe7e033312183a29bfa)
            check_type(argname="argument credential_spec", value=credential_spec, expected_type=type_hints["credential_spec"])
            check_type(argname="argument se_linux_context", value=se_linux_context, expected_type=type_hints["se_linux_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if credential_spec is not None:
            self._values["credential_spec"] = credential_spec
        if se_linux_context is not None:
            self._values["se_linux_context"] = se_linux_context

    @builtins.property
    def credential_spec(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"]:
        '''credential_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#credential_spec Service#credential_spec}
        '''
        result = self._values.get("credential_spec")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesCredentialSpec"], result)

    @builtins.property
    def se_linux_context(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]:
        '''se_linux_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#se_linux_context Service#se_linux_context}
        '''
        result = self._values.get("se_linux_context")
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivileges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    jsii_struct_bases=[],
    name_mapping={"file": "file", "registry": "registry"},
)
class ServiceTaskSpecContainerSpecPrivilegesCredentialSpec:
    def __init__(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Load credential spec from this file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file Service#file}
        :param registry: Load credential spec from this value in the Windows registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#registry Service#registry}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__131e53e08fec9ae7579208f1125d438e44cde662e6dc2ca32214b6814e9bc1a2)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file is not None:
            self._values["file"] = file
        if registry is not None:
            self._values["registry"] = registry

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''Load credential spec from this file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file Service#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry(self) -> typing.Optional[builtins.str]:
        '''Load credential spec from this value in the Windows registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#registry Service#registry}
        '''
        result = self._values.get("registry")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c6e2ce95e6f52ad199db53df9e21fe0caa911a5ad47ee4d981bf95757f1600)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetRegistry")
    def reset_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistry", []))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="registryInput")
    def registry_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryInput"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "file"))

    @file.setter
    def file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d652b2835b2a73b6ba16e1138af5d64b9b4062aefb2a29c27f77fe048a5230bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "file", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registry"))

    @registry.setter
    def registry(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5677a35675011aa442d3ba6f1334f02630088e9e34db9df7ed8e0a5005c3b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registry", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9540a61e2632c9c8cc4659b0feec69bf1824ae4294ee79852e5b202616ca1b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecPrivilegesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d4f2c5a7c78f0373dec2012f7ca9b8164f826283b9d34af07078d7e991e0b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCredentialSpec")
    def put_credential_spec(
        self,
        *,
        file: typing.Optional[builtins.str] = None,
        registry: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file: Load credential spec from this file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file Service#file}
        :param registry: Load credential spec from this value in the Windows registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#registry Service#registry}
        '''
        value = ServiceTaskSpecContainerSpecPrivilegesCredentialSpec(
            file=file, registry=registry
        )

        return typing.cast(None, jsii.invoke(self, "putCredentialSpec", [value]))

    @jsii.member(jsii_name="putSeLinuxContext")
    def put_se_linux_context(
        self,
        *,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable: Disable SELinux. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#disable Service#disable}
        :param level: SELinux level label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#level Service#level}
        :param role: SELinux role label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#role Service#role}
        :param type: SELinux type label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#type Service#type}
        :param user: SELinux user label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        value = ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(
            disable=disable, level=level, role=role, type=type, user=user
        )

        return typing.cast(None, jsii.invoke(self, "putSeLinuxContext", [value]))

    @jsii.member(jsii_name="resetCredentialSpec")
    def reset_credential_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentialSpec", []))

    @jsii.member(jsii_name="resetSeLinuxContext")
    def reset_se_linux_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeLinuxContext", []))

    @builtins.property
    @jsii.member(jsii_name="credentialSpec")
    def credential_spec(
        self,
    ) -> ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference, jsii.get(self, "credentialSpec"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxContext")
    def se_linux_context(
        self,
    ) -> "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference":
        return typing.cast("ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference", jsii.get(self, "seLinuxContext"))

    @builtins.property
    @jsii.member(jsii_name="credentialSpecInput")
    def credential_spec_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec], jsii.get(self, "credentialSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="seLinuxContextInput")
    def se_linux_context_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"]:
        return typing.cast(typing.Optional["ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext"], jsii.get(self, "seLinuxContextInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecContainerSpecPrivileges]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivileges], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivileges],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e53a9201e38af527339a37e5bc82156047d072ba7c3d53103ef79477183b4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    jsii_struct_bases=[],
    name_mapping={
        "disable": "disable",
        "level": "level",
        "role": "role",
        "type": "type",
        "user": "user",
    },
)
class ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext:
    def __init__(
        self,
        *,
        disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        level: typing.Optional[builtins.str] = None,
        role: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disable: Disable SELinux. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#disable Service#disable}
        :param level: SELinux level label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#level Service#level}
        :param role: SELinux role label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#role Service#role}
        :param type: SELinux type label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#type Service#type}
        :param user: SELinux user label. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__254d3b8aeac17082f30931cb771b0cc2344ecfcf7f36f33769dbd545d0823754)
            check_type(argname="argument disable", value=disable, expected_type=type_hints["disable"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable is not None:
            self._values["disable"] = disable
        if level is not None:
            self._values["level"] = level
        if role is not None:
            self._values["role"] = role
        if type is not None:
            self._values["type"] = type
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def disable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable SELinux.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#disable Service#disable}
        '''
        result = self._values.get("disable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''SELinux level label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#level Service#level}
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''SELinux role label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#role Service#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''SELinux type label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#type Service#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''SELinux user label.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d2eb0fa88d491a35e234a830bdc6fa727fbdd09adab5c2bc9440200ac2f76b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisable")
    def reset_disable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisable", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="disableInput")
    def disable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="disable")
    def disable(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disable"))

    @disable.setter
    def disable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debae7fc5aa795d8ac3f3e8a400fbfd945994824fdb6c68381cba782383ab0d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d02582404eb877613ea821680782f52cdf18a6a3b201a7e3ce5ec6c5e56c4f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4214d8ed502d438df21ec11a939ce0798eaa286a257df544a71fda200a23976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864b1c74bed0bc8306b6251217653acb6c77c6078f1f652331f3c484911aa886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ccb625ae418999c22a801cfb154e07a6479ad6abed3413782da94f40f19cffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ff34c28c4a13282de02324672f4353d4cb93049797f2df37618e31a9b9b056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "file_name": "fileName",
        "secret_id": "secretId",
        "file_gid": "fileGid",
        "file_mode": "fileMode",
        "file_uid": "fileUid",
        "secret_name": "secretName",
    },
)
class ServiceTaskSpecContainerSpecSecrets:
    def __init__(
        self,
        *,
        file_name: builtins.str,
        secret_id: builtins.str,
        file_gid: typing.Optional[builtins.str] = None,
        file_mode: typing.Optional[jsii.Number] = None,
        file_uid: typing.Optional[builtins.str] = None,
        secret_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param file_name: Represents the final filename in the filesystem. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_name Service#file_name}
        :param secret_id: ID of the specific secret that we're referencing. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secret_id Service#secret_id}
        :param file_gid: Represents the file GID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_gid Service#file_gid}
        :param file_mode: Represents represents the FileMode of the file. Defaults to ``0o444``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_mode Service#file_mode}
        :param file_uid: Represents the file UID. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_uid Service#file_uid}
        :param secret_name: Name of the secret that this references, but this is just provided for lookup/display purposes. The config in the reference will be identified by its ID Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secret_name Service#secret_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f412006b7228b76c7c064fb5d2c28a3494a40fc5a6e3ecad65276c55deb4611b)
            check_type(argname="argument file_name", value=file_name, expected_type=type_hints["file_name"])
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument file_gid", value=file_gid, expected_type=type_hints["file_gid"])
            check_type(argname="argument file_mode", value=file_mode, expected_type=type_hints["file_mode"])
            check_type(argname="argument file_uid", value=file_uid, expected_type=type_hints["file_uid"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_name": file_name,
            "secret_id": secret_id,
        }
        if file_gid is not None:
            self._values["file_gid"] = file_gid
        if file_mode is not None:
            self._values["file_mode"] = file_mode
        if file_uid is not None:
            self._values["file_uid"] = file_uid
        if secret_name is not None:
            self._values["secret_name"] = secret_name

    @builtins.property
    def file_name(self) -> builtins.str:
        '''Represents the final filename in the filesystem.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_name Service#file_name}
        '''
        result = self._values.get("file_name")
        assert result is not None, "Required property 'file_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''ID of the specific secret that we're referencing.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secret_id Service#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_gid(self) -> typing.Optional[builtins.str]:
        '''Represents the file GID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_gid Service#file_gid}
        '''
        result = self._values.get("file_gid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_mode(self) -> typing.Optional[jsii.Number]:
        '''Represents represents the FileMode of the file. Defaults to ``0o444``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_mode Service#file_mode}
        '''
        result = self._values.get("file_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def file_uid(self) -> typing.Optional[builtins.str]:
        '''Represents the file UID. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#file_uid Service#file_uid}
        '''
        result = self._values.get("file_uid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''Name of the secret that this references, but this is just provided for lookup/display purposes.

        The config in the reference will be identified by its ID

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secret_name Service#secret_name}
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecContainerSpecSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecContainerSpecSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecSecretsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6128e489c639c5f5606ff02eb283b5aa2da9161f0ba58e4746c31781044fd6eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecContainerSpecSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb68fbbedbfbf6d24de9ba07ee49488be184be18207d0cf0e1081b94e23343ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecContainerSpecSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07442c58549902552cc6adeeac13e662313e3ea4ed6c55b5349ba7022c00d038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c581da8e35de3b77fdcb545d0558e9fede5b8320f5fd3de6b053157ece0b9e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfaeb7b52d4c7494e6d122f3804f86dd9361cc9a9fca99762495fcca4a11a83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1276d4afe39c3e6885b34a906dc1c716a0bd6b5ee97e13031567c1214fbadfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecContainerSpecSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecContainerSpecSecretsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d4a178db55677a5b428e859fad5b6d1072c614efc7775266a5049ea36fa01f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFileGid")
    def reset_file_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileGid", []))

    @jsii.member(jsii_name="resetFileMode")
    def reset_file_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileMode", []))

    @jsii.member(jsii_name="resetFileUid")
    def reset_file_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUid", []))

    @jsii.member(jsii_name="resetSecretName")
    def reset_secret_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretName", []))

    @builtins.property
    @jsii.member(jsii_name="fileGidInput")
    def file_gid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileGidInput"))

    @builtins.property
    @jsii.member(jsii_name="fileModeInput")
    def file_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fileModeInput"))

    @builtins.property
    @jsii.member(jsii_name="fileNameInput")
    def file_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUidInput")
    def file_uid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileUidInput"))

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretNameInput")
    def secret_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretNameInput"))

    @builtins.property
    @jsii.member(jsii_name="fileGid")
    def file_gid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileGid"))

    @file_gid.setter
    def file_gid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5faa7ce39ef5aa42238dfb160040536b46569c58967e1221678ede2c36bb2ff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileMode")
    def file_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fileMode"))

    @file_mode.setter
    def file_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2ef04d3872bf8057498985eaf9b53c50770e5ad93e7733bbbc39b43b7a9c38f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileName")
    def file_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileName"))

    @file_name.setter
    def file_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85a520180314087362957cbfad1031a8e0aa2dc8ddba903974de2aa6122546c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUid")
    def file_uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileUid"))

    @file_uid.setter
    def file_uid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6711354182ba8d69c0c6f9f8f5298db4fec7d2dfdf574426ff7a1e18a2788da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66ddea3a9e039d8fa7a6925a69430e7d0933ef5e5d30e0c28fd6fe9be6c55c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @secret_name.setter
    def secret_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441f32a325fdea7b03d43644550e2cdb0cf55413aec0d461abef229ade2fe6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300074047904645e1e6f2ad306100d1abc3e74b05e533b31f210c1849abb5334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecLogDriver",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "options": "options"},
)
class ServiceTaskSpecLogDriver:
    def __init__(
        self,
        *,
        name: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The logging driver to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param options: The options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbd929ea7551fb3075150c10da1eff5c5cda0f1cb8bc94922ea31a092ccd76d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if options is not None:
            self._values["options"] = options

    @builtins.property
    def name(self) -> builtins.str:
        '''The logging driver to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The options for the logging driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecLogDriver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecLogDriverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecLogDriverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b5ac0eb8d0e43f156af2c575fd450f0479a24036f5da1281f211b9ab5b063c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b66ef38c5aaa07a2a1c0cceb5e6d0cedef8063e5a447b45f818bf0cff07392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa17f2d12944d0405d4bad4bca7320dd914e3190c5abdd5cf005c7cd353bae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecLogDriver]:
        return typing.cast(typing.Optional[ServiceTaskSpecLogDriver], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecLogDriver]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b86d3e19445354139af150bfb4e374947e1ee460751f589f8e821b2591f7551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecNetworksAdvanced",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "aliases": "aliases", "driver_opts": "driverOpts"},
)
class ServiceTaskSpecNetworksAdvanced:
    def __init__(
        self,
        *,
        name: builtins.str,
        aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
        driver_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name/id of the network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param aliases: The network aliases of the container in the specific network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#aliases Service#aliases}
        :param driver_opts: An array of driver options for the network, e.g. ``opts1=value``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_opts Service#driver_opts}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af86d732f02537efdfc19482334260392b85c88db9ac68421ef47b1fd802991)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
            check_type(argname="argument driver_opts", value=driver_opts, expected_type=type_hints["driver_opts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if aliases is not None:
            self._values["aliases"] = aliases
        if driver_opts is not None:
            self._values["driver_opts"] = driver_opts

    @builtins.property
    def name(self) -> builtins.str:
        '''The name/id of the network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The network aliases of the container in the specific network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#aliases Service#aliases}
        '''
        result = self._values.get("aliases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def driver_opts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of driver options for the network, e.g. ``opts1=value``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#driver_opts Service#driver_opts}
        '''
        result = self._values.get("driver_opts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecNetworksAdvanced(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecNetworksAdvancedList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecNetworksAdvancedList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1469f6a92ec6f955b8b6788209738f29fe58c9dd40955dd5be5ca383e66180e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecNetworksAdvancedOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25938098af537690526d615efeb48d98640e07d89cea50342ca91b4e0ac47d6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecNetworksAdvancedOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0a4223e84b2e57fe354f8591d50727c3411f016dafe5c75a026a39fef314e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b9c39d63a3a0115e9dfb3e5b6784e4cb9a31b985afc9b12b5c4413f79f712f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924afbe57660e7270b8cb1ea96e2d69a8ebb3ddcf67a886597a21ba0d4a5370e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cb6fb1a065e24f82f3e9801d1c2750f4d863c711d54ca856c103975c0d5105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecNetworksAdvancedOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecNetworksAdvancedOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed6b0df8dbe5294a16687cf58efe5ed8049234549331cbfc75230f23803e654)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAliases")
    def reset_aliases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAliases", []))

    @jsii.member(jsii_name="resetDriverOpts")
    def reset_driver_opts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDriverOpts", []))

    @builtins.property
    @jsii.member(jsii_name="aliasesInput")
    def aliases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "aliasesInput"))

    @builtins.property
    @jsii.member(jsii_name="driverOptsInput")
    def driver_opts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "driverOptsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="aliases")
    def aliases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "aliases"))

    @aliases.setter
    def aliases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5e8264937b292c3379fd11041c63f2b5e43d1dfa4d9269cb8ae3b6a0869328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aliases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="driverOpts")
    def driver_opts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "driverOpts"))

    @driver_opts.setter
    def driver_opts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304d3646766503fbcd231a5ff3ef4b34686a7cda39cb8217363a9d7f8c9238a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverOpts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc065d38a7e99fceb2d7c5d9d8e7a6b5dc567b4a2a4985c8f5f042684fcd110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5df6a34ac5dc480eafde4f9b8a9c674bf28d670dfe32dfccc7efec6ded892fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22d1ad1fee972a0a4031a2d4070ff3bca4dcd07c596023e150fe3ae1eefaa1cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerSpec")
    def put_container_spec(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        cap_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        cap_drop: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dir: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecDnsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        healthcheck: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
        hostname: typing.Optional[builtins.str] = None,
        hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        isolation: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
        privileges: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivileges, typing.Dict[builtins.str, typing.Any]]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
        stop_grace_period: typing.Optional[builtins.str] = None,
        stop_signal: typing.Optional[builtins.str] = None,
        sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: The image name to use for the containers of the service, like ``nginx:1.17.6``. Also use the data-source or resource of ``docker_image`` with the ``repo_digest`` or ``docker_registry_image`` with the ``name`` attribute for this, as shown in the examples. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#image Service#image}
        :param args: Arguments to the command. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#args Service#args}
        :param cap_add: List of Linux capabilities to add to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_add Service#cap_add}
        :param cap_drop: List of Linux capabilities to drop from the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#cap_drop Service#cap_drop}
        :param command: The command/entrypoint to be run in the image. According to the `docker cli <https://github.com/docker/cli/blob/v20.10.7/cli/command/service/opts.go#L705>`_ the override of the entrypoint is also passed to the ``command`` property and there is no ``entrypoint`` attribute in the ``ContainerSpec`` of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#command Service#command}
        :param configs: configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#configs Service#configs}
        :param dir: The working directory for commands to run in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dir Service#dir}
        :param dns_config: dns_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#dns_config Service#dns_config}
        :param env: A list of environment variables in the form VAR="value". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#env Service#env}
        :param groups: A list of additional groups that the container process will run as. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#groups Service#groups}
        :param healthcheck: healthcheck block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#healthcheck Service#healthcheck}
        :param hostname: The hostname to use for the container, as a valid RFC 1123 hostname. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hostname Service#hostname}
        :param hosts: hosts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#hosts Service#hosts}
        :param isolation: Isolation technology of the containers running the service. (Windows only). Defaults to ``default``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#isolation Service#isolation}
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#labels Service#labels}
        :param mounts: mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#mounts Service#mounts}
        :param privileges: privileges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#privileges Service#privileges}
        :param read_only: Mount the container's root filesystem as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#read_only Service#read_only}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#secrets Service#secrets}
        :param stop_grace_period: Amount of time to wait for the container to terminate before forcefully removing it (ms|s|m|h). If not specified or '0s' the destroy will not check if all tasks/containers of the service terminate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_grace_period Service#stop_grace_period}
        :param stop_signal: Signal to stop the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#stop_signal Service#stop_signal}
        :param sysctl: Sysctls config (Linux only). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#sysctl Service#sysctl}
        :param user: The user inside the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#user Service#user}
        '''
        value = ServiceTaskSpecContainerSpec(
            image=image,
            args=args,
            cap_add=cap_add,
            cap_drop=cap_drop,
            command=command,
            configs=configs,
            dir=dir,
            dns_config=dns_config,
            env=env,
            groups=groups,
            healthcheck=healthcheck,
            hostname=hostname,
            hosts=hosts,
            isolation=isolation,
            labels=labels,
            mounts=mounts,
            privileges=privileges,
            read_only=read_only,
            secrets=secrets,
            stop_grace_period=stop_grace_period,
            stop_signal=stop_signal,
            sysctl=sysctl,
            user=user,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerSpec", [value]))

    @jsii.member(jsii_name="putLogDriver")
    def put_log_driver(
        self,
        *,
        name: builtins.str,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param name: The logging driver to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#name Service#name}
        :param options: The options for the logging driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#options Service#options}
        '''
        value = ServiceTaskSpecLogDriver(name=name, options=options)

        return typing.cast(None, jsii.invoke(self, "putLogDriver", [value]))

    @jsii.member(jsii_name="putNetworksAdvanced")
    def put_networks_advanced(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9757bf628f0655289ea2e0368b796904abdc5bb71d4db4d3cf407407c01bc53f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworksAdvanced", [value]))

    @jsii.member(jsii_name="putPlacement")
    def put_placement(
        self,
        *,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param constraints: An array of constraints. e.g.: ``node.role==manager``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#constraints Service#constraints}
        :param max_replicas: Maximum number of replicas for per node (default value is ``0``, which is unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_replicas Service#max_replicas}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#platforms Service#platforms}
        :param prefs: Preferences provide a way to make the scheduler aware of factors such as topology. They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#prefs Service#prefs}
        '''
        value = ServiceTaskSpecPlacement(
            constraints=constraints,
            max_replicas=max_replicas,
            platforms=platforms,
            prefs=prefs,
        )

        return typing.cast(None, jsii.invoke(self, "putPlacement", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        limits: typing.Optional[typing.Union["ServiceTaskSpecResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        reservation: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#limits Service#limits}
        :param reservation: reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#reservation Service#reservation}
        '''
        value = ServiceTaskSpecResources(limits=limits, reservation=reservation)

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putRestartPolicy")
    def put_restart_policy(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        delay: typing.Optional[builtins.str] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param condition: Condition for restart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#condition Service#condition}
        :param delay: Delay between restart attempts (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param max_attempts: Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_attempts Service#max_attempts}
        :param window: The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#window Service#window}
        '''
        value = ServiceTaskSpecRestartPolicy(
            condition=condition, delay=delay, max_attempts=max_attempts, window=window
        )

        return typing.cast(None, jsii.invoke(self, "putRestartPolicy", [value]))

    @jsii.member(jsii_name="resetForceUpdate")
    def reset_force_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceUpdate", []))

    @jsii.member(jsii_name="resetLogDriver")
    def reset_log_driver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogDriver", []))

    @jsii.member(jsii_name="resetNetworksAdvanced")
    def reset_networks_advanced(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworksAdvanced", []))

    @jsii.member(jsii_name="resetPlacement")
    def reset_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacement", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetRestartPolicy")
    def reset_restart_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestartPolicy", []))

    @jsii.member(jsii_name="resetRuntime")
    def reset_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntime", []))

    @builtins.property
    @jsii.member(jsii_name="containerSpec")
    def container_spec(self) -> ServiceTaskSpecContainerSpecOutputReference:
        return typing.cast(ServiceTaskSpecContainerSpecOutputReference, jsii.get(self, "containerSpec"))

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> ServiceTaskSpecLogDriverOutputReference:
        return typing.cast(ServiceTaskSpecLogDriverOutputReference, jsii.get(self, "logDriver"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvanced")
    def networks_advanced(self) -> ServiceTaskSpecNetworksAdvancedList:
        return typing.cast(ServiceTaskSpecNetworksAdvancedList, jsii.get(self, "networksAdvanced"))

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> "ServiceTaskSpecPlacementOutputReference":
        return typing.cast("ServiceTaskSpecPlacementOutputReference", jsii.get(self, "placement"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "ServiceTaskSpecResourcesOutputReference":
        return typing.cast("ServiceTaskSpecResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="restartPolicy")
    def restart_policy(self) -> "ServiceTaskSpecRestartPolicyOutputReference":
        return typing.cast("ServiceTaskSpecRestartPolicyOutputReference", jsii.get(self, "restartPolicy"))

    @builtins.property
    @jsii.member(jsii_name="containerSpecInput")
    def container_spec_input(self) -> typing.Optional[ServiceTaskSpecContainerSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpecContainerSpec], jsii.get(self, "containerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdateInput")
    def force_update_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "forceUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="logDriverInput")
    def log_driver_input(self) -> typing.Optional[ServiceTaskSpecLogDriver]:
        return typing.cast(typing.Optional[ServiceTaskSpecLogDriver], jsii.get(self, "logDriverInput"))

    @builtins.property
    @jsii.member(jsii_name="networksAdvancedInput")
    def networks_advanced_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]], jsii.get(self, "networksAdvancedInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(self) -> typing.Optional["ServiceTaskSpecPlacement"]:
        return typing.cast(typing.Optional["ServiceTaskSpecPlacement"], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional["ServiceTaskSpecResources"]:
        return typing.cast(typing.Optional["ServiceTaskSpecResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="restartPolicyInput")
    def restart_policy_input(self) -> typing.Optional["ServiceTaskSpecRestartPolicy"]:
        return typing.cast(typing.Optional["ServiceTaskSpecRestartPolicy"], jsii.get(self, "restartPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInput")
    def runtime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeInput"))

    @builtins.property
    @jsii.member(jsii_name="forceUpdate")
    def force_update(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "forceUpdate"))

    @force_update.setter
    def force_update(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447b424e6883ffd5216c2e5613cdcc992af6ec661f12260fd5ae158c9db77982)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceUpdate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtime")
    def runtime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtime"))

    @runtime.setter
    def runtime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b1ffe6a3ae68e3e1a84ec54436bb17c6dfae0b74c1d77a34263078276fa229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpec]:
        return typing.cast(typing.Optional[ServiceTaskSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00496d30257bfce34cfa0457a148843c0f3097da9dbf6e89d038c96b886edb3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecPlacement",
    jsii_struct_bases=[],
    name_mapping={
        "constraints": "constraints",
        "max_replicas": "maxReplicas",
        "platforms": "platforms",
        "prefs": "prefs",
    },
)
class ServiceTaskSpecPlacement:
    def __init__(
        self,
        *,
        constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_replicas: typing.Optional[jsii.Number] = None,
        platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
        prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param constraints: An array of constraints. e.g.: ``node.role==manager``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#constraints Service#constraints}
        :param max_replicas: Maximum number of replicas for per node (default value is ``0``, which is unlimited). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_replicas Service#max_replicas}
        :param platforms: platforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#platforms Service#platforms}
        :param prefs: Preferences provide a way to make the scheduler aware of factors such as topology. They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#prefs Service#prefs}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c398e8317b8b76f3a50f9ff2b9b9d2b842459b191d14c3dc937276fcedc48fb)
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument max_replicas", value=max_replicas, expected_type=type_hints["max_replicas"])
            check_type(argname="argument platforms", value=platforms, expected_type=type_hints["platforms"])
            check_type(argname="argument prefs", value=prefs, expected_type=type_hints["prefs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if constraints is not None:
            self._values["constraints"] = constraints
        if max_replicas is not None:
            self._values["max_replicas"] = max_replicas
        if platforms is not None:
            self._values["platforms"] = platforms
        if prefs is not None:
            self._values["prefs"] = prefs

    @builtins.property
    def constraints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of constraints. e.g.: ``node.role==manager``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#constraints Service#constraints}
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_replicas(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of replicas for per node (default value is ``0``, which is unlimited).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_replicas Service#max_replicas}
        '''
        result = self._values.get("max_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def platforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]]:
        '''platforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#platforms Service#platforms}
        '''
        result = self._values.get("platforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]], result)

    @builtins.property
    def prefs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Preferences provide a way to make the scheduler aware of factors such as topology.

        They are provided in order from highest to lowest precedence, e.g.: ``spread=node.role.manager``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#prefs Service#prefs}
        '''
        result = self._values.get("prefs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecPlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecPlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ef5e8aaf973fa907441962756fcdfcb7328fd489925e70924be6508da95a02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPlatforms")
    def put_platforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceTaskSpecPlacementPlatforms", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3c61857ee786a64a387dc4e7a197f6dfe72403da466aaf5c74ea70541622bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPlatforms", [value]))

    @jsii.member(jsii_name="resetConstraints")
    def reset_constraints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConstraints", []))

    @jsii.member(jsii_name="resetMaxReplicas")
    def reset_max_replicas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicas", []))

    @jsii.member(jsii_name="resetPlatforms")
    def reset_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatforms", []))

    @jsii.member(jsii_name="resetPrefs")
    def reset_prefs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefs", []))

    @builtins.property
    @jsii.member(jsii_name="platforms")
    def platforms(self) -> "ServiceTaskSpecPlacementPlatformsList":
        return typing.cast("ServiceTaskSpecPlacementPlatformsList", jsii.get(self, "platforms"))

    @builtins.property
    @jsii.member(jsii_name="constraintsInput")
    def constraints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "constraintsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicasInput")
    def max_replicas_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicasInput"))

    @builtins.property
    @jsii.member(jsii_name="platformsInput")
    def platforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceTaskSpecPlacementPlatforms"]]], jsii.get(self, "platformsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefsInput")
    def prefs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "prefsInput"))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171fc25f6bf060ea6f55313ea3241cd17894364fa33e146551c1b1ecd11f777d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxReplicas")
    def max_replicas(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicas"))

    @max_replicas.setter
    def max_replicas(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab42f48513ad807ab4262f1887f4876130078dddbb7b09b1a8db445fcae53830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicas", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefs")
    def prefs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "prefs"))

    @prefs.setter
    def prefs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a00072168fe4040b1497e66205f6822d42b6173d4f29d02c06b25383771f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecPlacement]:
        return typing.cast(typing.Optional[ServiceTaskSpecPlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecPlacement]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2da06140627ec70e45ca9872da6d469b6bc68ca6d7a3f03d826a8603b654a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecPlacementPlatforms",
    jsii_struct_bases=[],
    name_mapping={"architecture": "architecture", "os": "os"},
)
class ServiceTaskSpecPlacementPlatforms:
    def __init__(self, *, architecture: builtins.str, os: builtins.str) -> None:
        '''
        :param architecture: The architecture, e.g. ``amd64``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#architecture Service#architecture}
        :param os: The operation system, e.g. ``linux``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#os Service#os}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c8d701e93fba0b5ef24907df3455ac2869963d6441556a916089ed878354744)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "architecture": architecture,
            "os": os,
        }

    @builtins.property
    def architecture(self) -> builtins.str:
        '''The architecture, e.g. ``amd64``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#architecture Service#architecture}
        '''
        result = self._values.get("architecture")
        assert result is not None, "Required property 'architecture' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os(self) -> builtins.str:
        '''The operation system, e.g. ``linux``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#os Service#os}
        '''
        result = self._values.get("os")
        assert result is not None, "Required property 'os' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecPlacementPlatforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecPlacementPlatformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecPlacementPlatformsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b23d9a6340cb053a9b697374f294be38c9539e67414237ed9f3a7eb6d7afe86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceTaskSpecPlacementPlatformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b40c62c539228e6c9663ebc5119f55b64430a1184d8c6c707ffa403b7bb15d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceTaskSpecPlacementPlatformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__762f24acc0f058e61e9efe635276b8561cc4dadc0ca4b12d8ec51321d4574d58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffaeecd846e6479f4e10a4b1bf2062565e3c5f200ebc3aa7710da5abe9386751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8470bd05dfed6f6fca0b8786ab4273ded46d935b6a7bfa5c0a6961fa0ac3edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__632e85caaa6b4d70ab66880f62e2792a4ce00ccbd7b9df2a5b3e082c15016da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecPlacementPlatformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecPlacementPlatformsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca81ad7b806a50f1be15acf57278677705f913f46421c9f38cc2291f2e3a3f80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208b2eec433f6f2a1735ab4240998c6dd576509a8170c7ca84554df16eef46f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cb0b7c7023c94416c63227fbab2a29ad5ef955de218bf2ede9a34cfdd26496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa297aa6297ac4fdb14913ae6fb6297bff9228b0073d8ed37f485acf828b7237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits", "reservation": "reservation"},
)
class ServiceTaskSpecResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Union["ServiceTaskSpecResourcesLimits", typing.Dict[builtins.str, typing.Any]]] = None,
        reservation: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param limits: limits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#limits Service#limits}
        :param reservation: reservation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#reservation Service#reservation}
        '''
        if isinstance(limits, dict):
            limits = ServiceTaskSpecResourcesLimits(**limits)
        if isinstance(reservation, dict):
            reservation = ServiceTaskSpecResourcesReservation(**reservation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86e293b3f81a79db6ce44de0de5777883fe56e9f235f6240c895fb357afa5ec)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument reservation", value=reservation, expected_type=type_hints["reservation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits
        if reservation is not None:
            self._values["reservation"] = reservation

    @builtins.property
    def limits(self) -> typing.Optional["ServiceTaskSpecResourcesLimits"]:
        '''limits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#limits Service#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesLimits"], result)

    @builtins.property
    def reservation(self) -> typing.Optional["ServiceTaskSpecResourcesReservation"]:
        '''reservation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#reservation Service#reservation}
        '''
        result = self._values.get("reservation")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesLimits",
    jsii_struct_bases=[],
    name_mapping={"memory_bytes": "memoryBytes", "nano_cpus": "nanoCpus"},
)
class ServiceTaskSpecResourcesLimits:
    def __init__(
        self,
        *,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bfc372d64b112ac91ab5306dbdb7c310bf572a7de9613513fcc1e195ad57ce)
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument nano_cpus", value=nano_cpus, expected_type=type_hints["nano_cpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        '''The amounf of memory in bytes the container allocates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        '''CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        result = self._values.get("nano_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecResourcesLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ad85cfb3bee08ea41923e289792e235c5dd24056db225f9885305ae601b6aab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMemoryBytes")
    def reset_memory_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryBytes", []))

    @jsii.member(jsii_name="resetNanoCpus")
    def reset_nano_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanoCpus", []))

    @builtins.property
    @jsii.member(jsii_name="memoryBytesInput")
    def memory_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanoCpusInput")
    def nano_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanoCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytes")
    def memory_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryBytes"))

    @memory_bytes.setter
    def memory_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4ad4d720a8533f0b02cbb45cfda0c2fd6ea2afbdb3fd30e95bb7b605273216a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanoCpus")
    def nano_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanoCpus"))

    @nano_cpus.setter
    def nano_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ed2b84f255a146752d4e124f45d9e82d9bef20b82b0e0b6785ef3a5d0ab764)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanoCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResourcesLimits]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesLimits], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesLimits],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f567b2c4dd2b51bbc3b1cb5fa838946e0ecd547aeba4391a00055d34ae2fce3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e6504cc76ebe6f4dbc47c9ab4ec0f35710f4b8c142c3bb61a1e28065e263dfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLimits")
    def put_limits(
        self,
        *,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of ``1/1e9`` (or ``10^-9``) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        value = ServiceTaskSpecResourcesLimits(
            memory_bytes=memory_bytes, nano_cpus=nano_cpus
        )

        return typing.cast(None, jsii.invoke(self, "putLimits", [value]))

    @jsii.member(jsii_name="putReservation")
    def put_reservation(
        self,
        *,
        generic_resources: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservationGenericResources", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param generic_resources: generic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#generic_resources Service#generic_resources}
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        value = ServiceTaskSpecResourcesReservation(
            generic_resources=generic_resources,
            memory_bytes=memory_bytes,
            nano_cpus=nano_cpus,
        )

        return typing.cast(None, jsii.invoke(self, "putReservation", [value]))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetReservation")
    def reset_reservation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservation", []))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> ServiceTaskSpecResourcesLimitsOutputReference:
        return typing.cast(ServiceTaskSpecResourcesLimitsOutputReference, jsii.get(self, "limits"))

    @builtins.property
    @jsii.member(jsii_name="reservation")
    def reservation(self) -> "ServiceTaskSpecResourcesReservationOutputReference":
        return typing.cast("ServiceTaskSpecResourcesReservationOutputReference", jsii.get(self, "reservation"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(self) -> typing.Optional[ServiceTaskSpecResourcesLimits]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesLimits], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="reservationInput")
    def reservation_input(
        self,
    ) -> typing.Optional["ServiceTaskSpecResourcesReservation"]:
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservation"], jsii.get(self, "reservationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceTaskSpecResources]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be0dfddb64a6f3894d736c1ac32cd2d7dd7854322fed06cabae2bb527c96291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesReservation",
    jsii_struct_bases=[],
    name_mapping={
        "generic_resources": "genericResources",
        "memory_bytes": "memoryBytes",
        "nano_cpus": "nanoCpus",
    },
)
class ServiceTaskSpecResourcesReservation:
    def __init__(
        self,
        *,
        generic_resources: typing.Optional[typing.Union["ServiceTaskSpecResourcesReservationGenericResources", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_bytes: typing.Optional[jsii.Number] = None,
        nano_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param generic_resources: generic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#generic_resources Service#generic_resources}
        :param memory_bytes: The amounf of memory in bytes the container allocates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        :param nano_cpus: CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        if isinstance(generic_resources, dict):
            generic_resources = ServiceTaskSpecResourcesReservationGenericResources(**generic_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d900f057607f5600beaed52b46c1f9a1486d6e09ed34cbaa6f81d85d3722c2e)
            check_type(argname="argument generic_resources", value=generic_resources, expected_type=type_hints["generic_resources"])
            check_type(argname="argument memory_bytes", value=memory_bytes, expected_type=type_hints["memory_bytes"])
            check_type(argname="argument nano_cpus", value=nano_cpus, expected_type=type_hints["nano_cpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if generic_resources is not None:
            self._values["generic_resources"] = generic_resources
        if memory_bytes is not None:
            self._values["memory_bytes"] = memory_bytes
        if nano_cpus is not None:
            self._values["nano_cpus"] = nano_cpus

    @builtins.property
    def generic_resources(
        self,
    ) -> typing.Optional["ServiceTaskSpecResourcesReservationGenericResources"]:
        '''generic_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#generic_resources Service#generic_resources}
        '''
        result = self._values.get("generic_resources")
        return typing.cast(typing.Optional["ServiceTaskSpecResourcesReservationGenericResources"], result)

    @builtins.property
    def memory_bytes(self) -> typing.Optional[jsii.Number]:
        '''The amounf of memory in bytes the container allocates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#memory_bytes Service#memory_bytes}
        '''
        result = self._values.get("memory_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nano_cpus(self) -> typing.Optional[jsii.Number]:
        '''CPU shares in units of 1/1e9 (or 10^-9) of the CPU. Should be at least ``1000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#nano_cpus Service#nano_cpus}
        '''
        result = self._values.get("nano_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesReservationGenericResources",
    jsii_struct_bases=[],
    name_mapping={
        "discrete_resources_spec": "discreteResourcesSpec",
        "named_resources_spec": "namedResourcesSpec",
    },
)
class ServiceTaskSpecResourcesReservationGenericResources:
    def __init__(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
        named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param discrete_resources_spec: The Integer resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        :param named_resources_spec: The String resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5419282a07d2a3da2ad843918d7477743d624f3cb1fbd894f57758dd95e45ffb)
            check_type(argname="argument discrete_resources_spec", value=discrete_resources_spec, expected_type=type_hints["discrete_resources_spec"])
            check_type(argname="argument named_resources_spec", value=named_resources_spec, expected_type=type_hints["named_resources_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if discrete_resources_spec is not None:
            self._values["discrete_resources_spec"] = discrete_resources_spec
        if named_resources_spec is not None:
            self._values["named_resources_spec"] = named_resources_spec

    @builtins.property
    def discrete_resources_spec(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Integer resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        '''
        result = self._values.get("discrete_resources_spec")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def named_resources_spec(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The String resources.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        result = self._values.get("named_resources_spec")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecResourcesReservationGenericResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecResourcesReservationGenericResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesReservationGenericResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b37ddb1eb1bad0a948135c6df0d36392cf2148acaeb896c8ed6ea02d1acff43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiscreteResourcesSpec")
    def reset_discrete_resources_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscreteResourcesSpec", []))

    @jsii.member(jsii_name="resetNamedResourcesSpec")
    def reset_named_resources_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamedResourcesSpec", []))

    @builtins.property
    @jsii.member(jsii_name="discreteResourcesSpecInput")
    def discrete_resources_spec_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "discreteResourcesSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="namedResourcesSpecInput")
    def named_resources_spec_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "namedResourcesSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="discreteResourcesSpec")
    def discrete_resources_spec(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "discreteResourcesSpec"))

    @discrete_resources_spec.setter
    def discrete_resources_spec(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29f33b0a408a567b9c8b1cc655a5e099d2cd9059cf524566bd378f7662bca83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discreteResourcesSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namedResourcesSpec")
    def named_resources_spec(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "namedResourcesSpec"))

    @named_resources_spec.setter
    def named_resources_spec(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b56e9f6ad48e9f35635bd13369494820adf545132cd18c515b2841f78757ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namedResourcesSpec", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceTaskSpecResourcesReservationGenericResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservationGenericResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesReservationGenericResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97dbc1513607d1fa484b119089d7c2fb94cbcddcc6d47530f0f976db0420edcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceTaskSpecResourcesReservationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecResourcesReservationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7352e0aa5e0d0010647f0ef954963c21a3c8f5475aa064f1501e69692a81b650)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGenericResources")
    def put_generic_resources(
        self,
        *,
        discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
        named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param discrete_resources_spec: The Integer resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#discrete_resources_spec Service#discrete_resources_spec}
        :param named_resources_spec: The String resources. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#named_resources_spec Service#named_resources_spec}
        '''
        value = ServiceTaskSpecResourcesReservationGenericResources(
            discrete_resources_spec=discrete_resources_spec,
            named_resources_spec=named_resources_spec,
        )

        return typing.cast(None, jsii.invoke(self, "putGenericResources", [value]))

    @jsii.member(jsii_name="resetGenericResources")
    def reset_generic_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGenericResources", []))

    @jsii.member(jsii_name="resetMemoryBytes")
    def reset_memory_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemoryBytes", []))

    @jsii.member(jsii_name="resetNanoCpus")
    def reset_nano_cpus(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNanoCpus", []))

    @builtins.property
    @jsii.member(jsii_name="genericResources")
    def generic_resources(
        self,
    ) -> ServiceTaskSpecResourcesReservationGenericResourcesOutputReference:
        return typing.cast(ServiceTaskSpecResourcesReservationGenericResourcesOutputReference, jsii.get(self, "genericResources"))

    @builtins.property
    @jsii.member(jsii_name="genericResourcesInput")
    def generic_resources_input(
        self,
    ) -> typing.Optional[ServiceTaskSpecResourcesReservationGenericResources]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservationGenericResources], jsii.get(self, "genericResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytesInput")
    def memory_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "memoryBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="nanoCpusInput")
    def nano_cpus_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nanoCpusInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryBytes")
    def memory_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "memoryBytes"))

    @memory_bytes.setter
    def memory_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88df65653ba02379c74d09c7de8f18ace01eed3d29f6330da806ea4cddcb3f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memoryBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nanoCpus")
    def nano_cpus(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nanoCpus"))

    @nano_cpus.setter
    def nano_cpus(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98d9e8e12f0265c2e7dd0b37134a9d2a92320b4cc08303573fb273dbc8dca5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nanoCpus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecResourcesReservation]:
        return typing.cast(typing.Optional[ServiceTaskSpecResourcesReservation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecResourcesReservation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc94289794034f6f8974e5bd10955364a48a10b11b4c37ac9e6090f9b587533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecRestartPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "delay": "delay",
        "max_attempts": "maxAttempts",
        "window": "window",
    },
)
class ServiceTaskSpecRestartPolicy:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        delay: typing.Optional[builtins.str] = None,
        max_attempts: typing.Optional[jsii.Number] = None,
        window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param condition: Condition for restart. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#condition Service#condition}
        :param delay: Delay between restart attempts (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param max_attempts: Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_attempts Service#max_attempts}
        :param window: The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#window Service#window}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7437c814147be937c1c47997767ede5a1b259cdc4e3b1e6e5e193c646de50fdf)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument max_attempts", value=max_attempts, expected_type=type_hints["max_attempts"])
            check_type(argname="argument window", value=window, expected_type=type_hints["window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if delay is not None:
            self._values["delay"] = delay
        if max_attempts is not None:
            self._values["max_attempts"] = max_attempts
        if window is not None:
            self._values["window"] = window

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''Condition for restart.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#condition Service#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between restart attempts (ms|s|m|h).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_attempts(self) -> typing.Optional[jsii.Number]:
        '''Maximum attempts to restart a given container before giving up (default value is ``0``, which is ignored).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_attempts Service#max_attempts}
        '''
        result = self._values.get("max_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def window(self) -> typing.Optional[builtins.str]:
        '''The time window used to evaluate the restart policy (default value is ``0``, which is unbounded) (ms|s|m|h).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#window Service#window}
        '''
        result = self._values.get("window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceTaskSpecRestartPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceTaskSpecRestartPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceTaskSpecRestartPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70399785d868c8a7b63665143697f511a064ec8100a6a7d86365c420aa7fca0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetMaxAttempts")
    def reset_max_attempts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAttempts", []))

    @jsii.member(jsii_name="resetWindow")
    def reset_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindow", []))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAttemptsInput")
    def max_attempts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAttemptsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowInput")
    def window_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60ccdd67452b44e4bdfd53e9dc23aeb4ce92d772359a2269eb5ed37c69083b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e109976de65f959aadfe4a17c35cd37fa9c9760877007c9734a74bbf02bd516d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAttempts")
    def max_attempts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAttempts"))

    @max_attempts.setter
    def max_attempts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__522977757e9da66dfb31e8501d5bf874bfcf955a17de9b08ebc29cee6ef1b1dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAttempts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="window")
    def window(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "window"))

    @window.setter
    def window(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e49fa6c7878e3ff73dda90dee88d248e428aea6c78c3051f6044db433f775c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "window", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceTaskSpecRestartPolicy]:
        return typing.cast(typing.Optional[ServiceTaskSpecRestartPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceTaskSpecRestartPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a914df3ffe0d135d3dda47ccabe254795c23a121defc41c526c4b4acc718bac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktn/provider-docker.service.ServiceUpdateConfig",
    jsii_struct_bases=[],
    name_mapping={
        "delay": "delay",
        "failure_action": "failureAction",
        "max_failure_ratio": "maxFailureRatio",
        "monitor": "monitor",
        "order": "order",
        "parallelism": "parallelism",
    },
)
class ServiceUpdateConfig:
    def __init__(
        self,
        *,
        delay: typing.Optional[builtins.str] = None,
        failure_action: typing.Optional[builtins.str] = None,
        max_failure_ratio: typing.Optional[builtins.str] = None,
        monitor: typing.Optional[builtins.str] = None,
        order: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delay: Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        :param failure_action: Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        :param max_failure_ratio: Failure rate to tolerate during an update. Defaults to ``0.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        :param monitor: Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        :param order: Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        :param parallelism: Maximum number of tasks to be updated in one iteration. Defaults to ``1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c628a0c0d4e5e81f4dc17f6d7209e557d355883fbb98f565ffca41f75897c6e)
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
            check_type(argname="argument failure_action", value=failure_action, expected_type=type_hints["failure_action"])
            check_type(argname="argument max_failure_ratio", value=max_failure_ratio, expected_type=type_hints["max_failure_ratio"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delay is not None:
            self._values["delay"] = delay
        if failure_action is not None:
            self._values["failure_action"] = failure_action
        if max_failure_ratio is not None:
            self._values["max_failure_ratio"] = max_failure_ratio
        if monitor is not None:
            self._values["monitor"] = monitor
        if order is not None:
            self._values["order"] = order
        if parallelism is not None:
            self._values["parallelism"] = parallelism

    @builtins.property
    def delay(self) -> typing.Optional[builtins.str]:
        '''Delay between task updates ``(ns|us|ms|s|m|h)``. Defaults to ``0s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#delay Service#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failure_action(self) -> typing.Optional[builtins.str]:
        '''Action on update failure: ``pause``, ``continue`` or ``rollback``. Defaults to ``pause``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#failure_action Service#failure_action}
        '''
        result = self._values.get("failure_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_failure_ratio(self) -> typing.Optional[builtins.str]:
        '''Failure rate to tolerate during an update. Defaults to ``0.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#max_failure_ratio Service#max_failure_ratio}
        '''
        result = self._values.get("max_failure_ratio")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''Duration after each task update to monitor for failure (ns|us|ms|s|m|h). Defaults to ``5s``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#monitor Service#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def order(self) -> typing.Optional[builtins.str]:
        '''Update order: either 'stop-first' or 'start-first'. Defaults to ``stop-first``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#order Service#order}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of tasks to be updated in one iteration. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/kreuzwerker/docker/3.6.2/docs/resources/service#parallelism Service#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceUpdateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceUpdateConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktn/provider-docker.service.ServiceUpdateConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__651035cce54779bae6d3163f6c82a70e7e92e9cee562a1eb904681286a3535c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @jsii.member(jsii_name="resetFailureAction")
    def reset_failure_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureAction", []))

    @jsii.member(jsii_name="resetMaxFailureRatio")
    def reset_max_failure_ratio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxFailureRatio", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetOrder")
    def reset_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrder", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="failureActionInput")
    def failure_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "failureActionInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatioInput")
    def max_failure_ratio_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxFailureRatioInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delay"))

    @delay.setter
    def delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b198f127a27702f5925fc4c0de0ce1aca9c67086ead8d25ede9b36fe7e9f182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failureAction")
    def failure_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failureAction"))

    @failure_action.setter
    def failure_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d35840fb3b23d03a3e29cd67c8cf6031db6bb1693e4c9580239792055c7265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailureRatio")
    def max_failure_ratio(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxFailureRatio"))

    @max_failure_ratio.setter
    def max_failure_ratio(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb374aafda9a7c530b8bc8d85434af22421b5fadeea36d9a262d93eedd9f880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailureRatio", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @monitor.setter
    def monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45af0fbbc8911944d2d77ea75e7a867a773adbf7255adc1373c8503a1341c974)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "order"))

    @order.setter
    def order(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1624ea5554ed478103186b45adf1a9f59d4a708cbd16a4c1495f88a17f489322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b10cf8ed743de0dd11eaaccd9b398a4a2f6e40798d0ec2f922ca3cd72ad59a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceUpdateConfig]:
        return typing.cast(typing.Optional[ServiceUpdateConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceUpdateConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e6b5d77761966d099bff1406eda56313d90066dcc50bf5285f23a501f41879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Service",
    "ServiceAuth",
    "ServiceAuthOutputReference",
    "ServiceConfig",
    "ServiceConvergeConfig",
    "ServiceConvergeConfigOutputReference",
    "ServiceEndpointSpec",
    "ServiceEndpointSpecOutputReference",
    "ServiceEndpointSpecPorts",
    "ServiceEndpointSpecPortsList",
    "ServiceEndpointSpecPortsOutputReference",
    "ServiceLabels",
    "ServiceLabelsList",
    "ServiceLabelsOutputReference",
    "ServiceMode",
    "ServiceModeOutputReference",
    "ServiceModeReplicated",
    "ServiceModeReplicatedOutputReference",
    "ServiceRollbackConfig",
    "ServiceRollbackConfigOutputReference",
    "ServiceTaskSpec",
    "ServiceTaskSpecContainerSpec",
    "ServiceTaskSpecContainerSpecConfigs",
    "ServiceTaskSpecContainerSpecConfigsList",
    "ServiceTaskSpecContainerSpecConfigsOutputReference",
    "ServiceTaskSpecContainerSpecDnsConfig",
    "ServiceTaskSpecContainerSpecDnsConfigOutputReference",
    "ServiceTaskSpecContainerSpecHealthcheck",
    "ServiceTaskSpecContainerSpecHealthcheckOutputReference",
    "ServiceTaskSpecContainerSpecHosts",
    "ServiceTaskSpecContainerSpecHostsList",
    "ServiceTaskSpecContainerSpecHostsOutputReference",
    "ServiceTaskSpecContainerSpecLabels",
    "ServiceTaskSpecContainerSpecLabelsList",
    "ServiceTaskSpecContainerSpecLabelsOutputReference",
    "ServiceTaskSpecContainerSpecMounts",
    "ServiceTaskSpecContainerSpecMountsBindOptions",
    "ServiceTaskSpecContainerSpecMountsBindOptionsOutputReference",
    "ServiceTaskSpecContainerSpecMountsList",
    "ServiceTaskSpecContainerSpecMountsOutputReference",
    "ServiceTaskSpecContainerSpecMountsTmpfsOptions",
    "ServiceTaskSpecContainerSpecMountsTmpfsOptionsOutputReference",
    "ServiceTaskSpecContainerSpecMountsVolumeOptions",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsList",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsLabelsOutputReference",
    "ServiceTaskSpecContainerSpecMountsVolumeOptionsOutputReference",
    "ServiceTaskSpecContainerSpecOutputReference",
    "ServiceTaskSpecContainerSpecPrivileges",
    "ServiceTaskSpecContainerSpecPrivilegesCredentialSpec",
    "ServiceTaskSpecContainerSpecPrivilegesCredentialSpecOutputReference",
    "ServiceTaskSpecContainerSpecPrivilegesOutputReference",
    "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext",
    "ServiceTaskSpecContainerSpecPrivilegesSeLinuxContextOutputReference",
    "ServiceTaskSpecContainerSpecSecrets",
    "ServiceTaskSpecContainerSpecSecretsList",
    "ServiceTaskSpecContainerSpecSecretsOutputReference",
    "ServiceTaskSpecLogDriver",
    "ServiceTaskSpecLogDriverOutputReference",
    "ServiceTaskSpecNetworksAdvanced",
    "ServiceTaskSpecNetworksAdvancedList",
    "ServiceTaskSpecNetworksAdvancedOutputReference",
    "ServiceTaskSpecOutputReference",
    "ServiceTaskSpecPlacement",
    "ServiceTaskSpecPlacementOutputReference",
    "ServiceTaskSpecPlacementPlatforms",
    "ServiceTaskSpecPlacementPlatformsList",
    "ServiceTaskSpecPlacementPlatformsOutputReference",
    "ServiceTaskSpecResources",
    "ServiceTaskSpecResourcesLimits",
    "ServiceTaskSpecResourcesLimitsOutputReference",
    "ServiceTaskSpecResourcesOutputReference",
    "ServiceTaskSpecResourcesReservation",
    "ServiceTaskSpecResourcesReservationGenericResources",
    "ServiceTaskSpecResourcesReservationGenericResourcesOutputReference",
    "ServiceTaskSpecResourcesReservationOutputReference",
    "ServiceTaskSpecRestartPolicy",
    "ServiceTaskSpecRestartPolicyOutputReference",
    "ServiceUpdateConfig",
    "ServiceUpdateConfigOutputReference",
]

publication.publish()

def _typecheckingstub__21cb49c196354f919c566ae3e0ffcea09c2682023510f1ba79d99f59317958fa(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    task_spec: typing.Union[ServiceTaskSpec, typing.Dict[builtins.str, typing.Any]],
    auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    converge_config: typing.Optional[typing.Union[ServiceConvergeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_spec: typing.Optional[typing.Union[ServiceEndpointSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[typing.Union[ServiceMode, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback_config: typing.Optional[typing.Union[ServiceRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[ServiceUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e6762d0eba2e4fa258cedd385e5cfe12774d754bac429e647c967de743af5c25(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4e04342a7e60f6f14ca6abf03cc34722629bc87370808312b5dfb16369d309(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6522b7f59cb6f5199e43d6472fc36d6a9fb8ed44ed04775ce7988a5f6b6a2a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f026f3c5bd7c094670284db6f25f343a09da1d8d73e64c56e6b6e2bab8ad81e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9aea760943cefe39bf2f4c67ea8caec4f9b38ceb027ee64faff5db46376b287(
    *,
    server_address: builtins.str,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9acd31ab3db0059f772cfe75ec4c0fc49c4cbe62ba4976f33553dbf73885b0d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e88d9fdf235a7645e78c24c572906257dcb75d16c3884584121ca38bdda6fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ef46c0d34f114ce12109c552dc95b282d57ee21fee06de8866543c454434be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898e4d2e30e1392c7881d68eaf657ae9dbfd4c861b41cadd991b73d2e7b7ad63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39eb64684b9f0ecc2176aa86329077af1a112ca6a31fd983e22708e4df234e1(
    value: typing.Optional[ServiceAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3e7ecb041d517789e27c0692550c575bf9c57bb66d494a38497590dc354904(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    task_spec: typing.Union[ServiceTaskSpec, typing.Dict[builtins.str, typing.Any]],
    auth: typing.Optional[typing.Union[ServiceAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    converge_config: typing.Optional[typing.Union[ServiceConvergeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    endpoint_spec: typing.Optional[typing.Union[ServiceEndpointSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mode: typing.Optional[typing.Union[ServiceMode, typing.Dict[builtins.str, typing.Any]]] = None,
    rollback_config: typing.Optional[typing.Union[ServiceRollbackConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    update_config: typing.Optional[typing.Union[ServiceUpdateConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23210ffc14b693ac1e355a456926323e83361f73dfb530d88acbb6134fc0d9c(
    *,
    delay: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5831fc4f695b229dab50bbc733a72d14cfe132b5a3561d2db2917dcdb20907c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6317bbae03b08a624dcb552e4e668bd0db7f000f32f4d3e5242410cdf2eeed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b584aba92d1804e0e39b279fe17b0223cd3494973b2b7522d4a683a91544dd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e2795b6e36c0d57d96912a8cb27201ac1e463a444eddfa50249aa84145c35a(
    value: typing.Optional[ServiceConvergeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2556ea1982c3b1b57993776dab8b88c7c07e1449e2dfbd9fe683a33fd3db90(
    *,
    mode: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEndpointSpecPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0346c93556480682a560b3f49bafcdc20188046a43cb381b50daf1ffe0938fd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dc998a167b2ee7cb34c1015cfeaec871930987184e224910f04aea24edee77(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEndpointSpecPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c6641f4caa9d1a3c01ca5262c9d23ec7b4ef3944cd02054eb424fdcf46dd4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ad98d869fbfaace2a83cd718a298c1e18dd07fcc21d9fcb8346befc1d3ac56(
    value: typing.Optional[ServiceEndpointSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd409048b41082aafae84395c8220721d026ea9efcfd6c94010ab472be15877(
    *,
    target_port: jsii.Number,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    published_port: typing.Optional[jsii.Number] = None,
    publish_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2dbda225b8b63fa7166892710b592b434a26ef09b69715d088a8e1cd831d02b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b7d1eeb84b5338fce1ba635af1e2525b52a31f8025f0750ff8e553f985f1e31(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a46bb530ead74f68005059f25522433b6a0242b91d3721a8f69c58e975ed67b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238fa67ea7eb58fb0d8408af7d4009c811223b54d5e18b0d8391e29d1b688482(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68f2df94ea2e742b8e98911867f651c7254e6f032c02a68f00df4a53cc4c4a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4766144094e9457086870b609a5dc0d83069eb066441bd5edc6335dc2fa7b3cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEndpointSpecPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28e628e0914a64b8d4423b039f17d932710cfc279b305a9ecc9a1da43824a4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3160ff41bfbbca1cb0f1b5e591bcddc64ed7e3651014c3be249820f11150ffdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859f9cfcf5efac3350057ec250056df8dda3b5a86cbac49b47a1b0354d136038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055e18fcca13f3ab071f976ce666db2f6c36c10a1c7735a990039a101928e9b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2842bece6867e5534713542ab49d35b359178e05e4c0b4c22fd2cd84bbd6f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde9fca8ab5cfa202105881dbe096f46f000d64dfcccce7f9be20c3db10b3c28(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadebe95e21ffcaa6c1df3b5272289f8dcefd7365461ee3eddbe88af2c71b5ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEndpointSpecPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718759b785ee227441182ba9648060c5cbfa27860f45fab56e125b5f079ae7ba(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1fb3e414d6eb06ebb7782b8895b6c3f44ab7ccda06cd95e757ae944cb9b267(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf1431ee58a338bf3cf967c5f57006c3f933783f86badeeaae48f14d9cc009b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce27a149872579508e8bceaf65123705800e1e38e0f91369ab5babcce500932(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f3e5c51c26c8be8c12be1849676d1b99034e97b3c16a6bcaacc00adcc64944(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2d76c1cdba7ac3033394c3df5ea5a888ecc1241ba2af241518237c29469135(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c2fcab177c89d8e07be86e88563677b62cac6cace043579c9f88bb74a11d61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccac8d4c6c37d738ab2560ff9991a6b606f70380416db1d6992f8e56812501e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3f70d2efe0c9e515447c820cfeee444c9673307fd0a57b73310635a1c2a2f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cf2f9cde60680525e5257ecfd639f8d68b268cd1edecf7847cea52e4184901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d34f01350c32712e24af28798cb35bf21ae5214d00117dbf67fc61732c1d06(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eeee4162ddd2fa6575aa89be006cdd82a912a6ea38a0ad7d7d1a017e6397342(
    *,
    global_: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replicated: typing.Optional[typing.Union[ServiceModeReplicated, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce67e25e193bc9fbdd80d504076b5b2a1a8645e2a2260b30790158b09903c750(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033879d6c821a7e5730bf7e5ee5dd1ca520601f962ebe3f1314afb87e578dbde(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22db1e02983bc97bd85640043775289f4992827ae059ae7117bd9f15f37aad3(
    value: typing.Optional[ServiceMode],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9452e65cac37ffac3b0e95cd282e30ef133f31072208ea0997c371acbf8e0ffc(
    *,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb0628d3dae2bc901e5b8eaf66e1909d9ecf8d0dcc6315728df469a9db67df9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd77865a7cf4b122a8f4e9ed0be72898322146603589162814bce1160e063443(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e146850c888f2e84adb0059601447246b59552d72566f5ae8404dfb4dc6dc2b(
    value: typing.Optional[ServiceModeReplicated],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917bb9735b94339f11f066516eb3c40958edb6e7234c1ddc0de19050c2e6b727(
    *,
    delay: typing.Optional[builtins.str] = None,
    failure_action: typing.Optional[builtins.str] = None,
    max_failure_ratio: typing.Optional[builtins.str] = None,
    monitor: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a23196b99beaccdf59baf4ed8230e67e2e89ee86d41c3391d36f3ef1942778(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa00cb763d7ce3c42f0583ffc50fd1d44ea953ae96a7f7ed7dbda4df2b5781f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9b17b3fdf7478a63debab0d0d97ad5d9355052c188960230842cccf10c470c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f5539617fe2515c87f3558840aeea9358f7dd78afc47280d756ad7731800d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f0eb28d1c74e7d6f927ebf33cc1ab812498ad8783c6fc6ad3d7210903bd94a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a9e024a1c0d4f547cc6b5a7bac99da3d5de8f4efe67214f93a18aa408ee612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c013353840748671bc4738a24e51b77b0e2fa4fa4d94b4d2bcf677e0ba1f32af(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e372f2faab2138a91e6f66763b1b5a5c7729637a952f67a6fff2dc9c4e99a6(
    value: typing.Optional[ServiceRollbackConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830aa6e15ad5670e9a056cb802a29fb54a52e8b0c9d86ae956de92122be67cfe(
    *,
    container_spec: typing.Union[ServiceTaskSpecContainerSpec, typing.Dict[builtins.str, typing.Any]],
    force_update: typing.Optional[jsii.Number] = None,
    log_driver: typing.Optional[typing.Union[ServiceTaskSpecLogDriver, typing.Dict[builtins.str, typing.Any]]] = None,
    networks_advanced: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement: typing.Optional[typing.Union[ServiceTaskSpecPlacement, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[ServiceTaskSpecResources, typing.Dict[builtins.str, typing.Any]]] = None,
    restart_policy: typing.Optional[typing.Union[ServiceTaskSpecRestartPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf7797ac5369c042b72ebf4dca7e9cde9c6b303108ce7a022f98010ae9a71a3(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    cap_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    cap_drop: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dir: typing.Optional[builtins.str] = None,
    dns_config: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecDnsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    healthcheck: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecHealthcheck, typing.Dict[builtins.str, typing.Any]]] = None,
    hostname: typing.Optional[builtins.str] = None,
    hosts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    isolation: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    privileges: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivileges, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    stop_grace_period: typing.Optional[builtins.str] = None,
    stop_signal: typing.Optional[builtins.str] = None,
    sysctl: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d249dec05b44127fdc5898520f1e89582ced475cc99b3189caed2653f1d415(
    *,
    config_id: builtins.str,
    file_name: builtins.str,
    config_name: typing.Optional[builtins.str] = None,
    file_gid: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[jsii.Number] = None,
    file_uid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fbccc2c7f1e0b6d648ab69f0bd3436a4b416e45f59c7fce17a9327e02d4b88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe2638a4deb83fe4f0ef18ec58139815df573ba2abea9d65c299af6c9aa2cec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d876f5888266d862f575c1b392a051288a933b8d992f26432dd267025ed35d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590513d2abeae251f65f030cf307a219cc0940d7e0a9f8bd0e03b6b133e762c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a385e8a437ed7b65dd439514349a8e67eb80b11ee4d6dec1eb1c6154905345d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca76f68f95913963c095b42ab390f1d9b448bd4686fea6b0ea9997016d6c5b3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af8d8c6405785132cb5328173f4472d0b1e1eeac50381a31b5722fb6a662a83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fcf82a0ad78cd7e76089c467129fdc0ee2060143eeb67dc1475c4f2bf9dbf42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11e413f7dcbac71cd0492880cb01c009022e4273335fde32a573f1ee9563855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df74318797136516130074c12b0d5f83217164a7e8574e3178b9697c91a35bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d56bac005cb988cae3da456c7274c8de61f53e4eeabd3a2e9a77766328d6f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88e83b3285fce1a66e912c25e0eda563694726a3feb498ef33dad43fe21f0f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ad721fb2d71fe591293533b366af39b10e09763d914bb2db91aef6d6a55ddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765d9d758d63decc4b8e5785639e9dafef498efdb5413e15fc352e6f783412ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9abf56519b143da582c8f4c1019073b156be13dd67beaea1e5b9cfdf33288e(
    *,
    nameservers: typing.Sequence[builtins.str],
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    search: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b69de7bcf419b852f914f04a56fdc71194b43e12013b35a8e54bcf302c3a4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160710e15c898783dbae2a558ab4482704bb50aed0f4bc665066bdaa99b35c99(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aed0e1de60d7e5fadd28bd1ef474f3f5d06a010eebd282de09e04a0bb9246c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647ca625180d9c17aaf9c6b6ceb8124f6f19ec126fde358cd69bd5a0d5c17066(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a80c1127eece90366f6e360b01bc79a3ea7d9df3ee4a3ccdafce99d495941b0(
    value: typing.Optional[ServiceTaskSpecContainerSpecDnsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc05914071b7efa59cac5489c0ac4dd26e0a3efa5943fc0cbc1692bacdecd3f(
    *,
    test: typing.Sequence[builtins.str],
    interval: typing.Optional[builtins.str] = None,
    retries: typing.Optional[jsii.Number] = None,
    start_period: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb3ad99b5425671cf8428179d370f1b173bd98afeaecc8025a470654b901d18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868d2d536a14b4ed24bca8f976c1a8bcea10f12dde3f61714e817dc6914c3ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d28590fb82cc52dee8c6b2f35e92f6c3ead92bd30183b49de711e357e4aa1f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389295cd1df74a6c154f4b2c69b3ce00e8402463117443bc50dbe660336fcf1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6150461fada1c8deaed1a94c4a7dd12046ad706c2c8705cc9d606e7127ea4f1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e7030bbb48cb8fa58f0ee2e26dad0ce2f67708fe13dbcb6e11ad4f611188fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81e740fff23d35c391a241a9901573df43c9d0a0f59c215f598d8bb7589d953c(
    value: typing.Optional[ServiceTaskSpecContainerSpecHealthcheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bf1ec40a4ee60f8f8a74ab412827c3cfbc7421c9221619f4993f53fb0e83d1(
    *,
    host: builtins.str,
    ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbfc4daf99d95aa1fba30bd22812241677bff087b968ee7632b09f55088d3cd4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb47e7f3046a9f186e0e1b260bb156c8c8106fd1aeaca64ef5cf6f6730d8011(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9a9fba1de8f26e8b63aa74060ee8fbe840ca647769f601029cc25ab70eac7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e1ee69d0d93c3934e0ab8de8c490f6cc9c74d98934c6dda77c65c691edf401(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c14e1ce4606a4a98df5130c70bab695445e7ea6ede527d054555cf674a56a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc69681e20a855d3d3e888dbb4ba3aed082ea8ef6e59c76a89698140f85b7c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecHosts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75c8b8814ed8bf8e50f6041441462168285cc714e8d8804b70a40b547237c99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fa596ded4e77b84e395d1058b112371714331c525f65eb1b71c7766520b141(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b05553424f2e05f554d9fc80b6e45487822d197b897dce1ad41a67c0efe783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c5b293f720d943a5e2c12442fcb5a4ee590324f0c10d57ba9c56e8b50ee93a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecHosts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14636036c1dbc368581cfabb5969ca56f7ceb24a3832a12ea056e5870327b089(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7feecb6ba6cc9411f30ead2387ebc022d2abf0d8858dc522ba035546058c2907(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a470f69d5fee6ca660e1c0348ff8a4cef2841381eb7dc18248640af9a6c717ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc16981802bc4da75ea8ef089d79fe387a71e9be1f076ec4dd87959523f9e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246d2bf65facc0014ae0e157c8e2e260b62c5c58ded233bf548df82e693b2b1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a07ff2d459cb0a8440949877a7575e98e7909c3d352b6c3b612c728f398ecb1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8004a8f0422052bf9e7e60abf079cc7f599a10b389867212db6a92f958c54e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15a3f5198962dd4fb0a657b9fc28b56ce17c3cf29eb64b98186bd79bbc6b7b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e87045f1ff7789c556bcf3b3a82cad1aa39e6b2a7323108c9a782060d70782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bba8fef9fad1facefcd241682e6e70b684a0c4546e3159aba01ef32aba8e0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63344f3b810ffa96d47a7ae653943725a4a18e8a265f50cd61c7f4c76156a023(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e5b5738704c296c7808449c3a58dcd2b5bbaa8ef544378487e4f7f65944671(
    *,
    target: builtins.str,
    type: builtins.str,
    bind_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsBindOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
    tmpfs_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsTmpfsOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_options: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2484428e63894de3c13d4e21fc7e6462da0b323465e42cd7a69205daf6864cbd(
    *,
    propagation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51dd3e5a6159fdf9d80f1c7fc174192a5f63989b1c37c556a92ddd7878c6d2a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8165fb0c07b85b48653a7931c60284adf7077fb808ec629ff84f683b5eb21b0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8008e0cde8bb77fb27598b384bb9cde4e78649da17ee05c726ca1f8ca3679d(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsBindOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0392030cf0234a8cb380bf292ebd0b475d71637269e95fb552d4ada3492b405e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59aa9f7e9ec12d1c2119c3f594f852d7d7521ebd7723f6e2d96bd452d48a63d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74cbed61f07f28ca6281f04325f1946b1f78bb99fef81a192066053991498e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54685e714bccc9a5ad327943e3322ff5b372ba23f70c1b271bfec954ac0150eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caac5a69b8c51194ac1c22b80e850f8334d6a4b7540646bab05b7288e618cea9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bafb2c8bff1e1730e76f97719c27654cfecdf5d302ea6442705a6afe5aae70dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0958bd29798efe9e9748050b779c08b85440c3e17416307255478a95a5cd9c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb4f5d2ccbe0ad1149717af6804bfe5077523f7ac66b8ba19a9ea4ec6e6e1cc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43566ab5664f9386258b5f28940817fb5bc32789a5ace61ecd7241e5f7ae6f45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2069121e9d1c68c9bc7ebf4cb8ba1b7aa61029b3a0c173710e360dc47b3ca0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119434017910afab9b9095c050ad8ea9db4b9be75a36c48378993b55cf95df26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e4481c160c8e129ae0daa8ea41207a6a7ea7615687d726af3a4f47199e46c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e289b5c69fe84ef21048faa4e2d3cd2631260cde5f3c26f59895fd88bfe643a(
    *,
    mode: typing.Optional[jsii.Number] = None,
    size_bytes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d65d355ec0ada2d8003c92bb2b29dd6ff3914f921a56fdcb7ec0c20150833e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2532a415038a208c9640ac612ff93130d1c0f8148caaee46e1bf4d04c3c99e0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf38eae48913f49fc5aab6f94d34d818c5e95f204a390cdb6d99ef586c41b3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ebb98e76b0b0985a4e75f78154f83088a62598d1b69acf6e38193b93a4ce26(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsTmpfsOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af05a0939e31cb583eda3d82f21bbb8180d71ca426281ed5a0c1f2394a327cc(
    *,
    driver_name: typing.Optional[builtins.str] = None,
    driver_options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    no_copy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aae8df9f9ae986a5621822664a3fb2b5b9dea2a3f60afce5d44bb55017d447(
    *,
    label: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75081e5335b1dd9365c8b3963bcf061a3ae446d5d0f333be74668ee70d5ef0a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a08c8b3ca5df8f8e8fd8eecabc4d9c74fff9ad3ddb4d0aeb53a07846f338e4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f9677c94739f9acb2d8ff2d5ac6ae4a27f64f9945a5a41d231ac6161f9a176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cb9bb3024b1f2cb67c24207376209f93f6e43ab233a00da01bd5941a77adec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8446875f6a6a339814a54fa6ab05fb61af92bb07c4a8fb35ccd177229615724b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f11a25a0a8ff43b53a25268297d6eec0fd20f131fc8de5b99583b78a703e1b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26a12c601dd7560a45f82ca26ee5a2b0d7f58b2ab82ab7865f49db1f946c95d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a152fc24331f120bf430ce4a06b6b82988e1a7fd1b43b66d561657655055bfd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b0d496b0504bf38af7bfb9a374a904530e81f42662b5ac64841e0555421032(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb6259472aaa0d227bfeb0e2a7f482b1b1d07dfc29a54df4dbb596f312f192c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b911694987bf3755f29ae31e01fcc8e5fe24f4a67111a3867919a7e993637fcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85a4593f586424c70f632746476ba22475c97a4fe424ba059fd52e44ca633f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMountsVolumeOptionsLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68c7f62a60d9eaeb01bf468d0bbe3eae37820856fc6de80e4ea32e0327f163e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dd1a88f0b1f83e57b8f5b89af694388929bbae4973821b3301eca1036310f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e6136dab20d51f2eda610110bf14a8227e5e7c79489f13f0f682fb6a174dde(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf593e6cc7a673ce1dd22c7674af2f848b3e2f8b308c6bb2ad69800656152763(
    value: typing.Optional[ServiceTaskSpecContainerSpecMountsVolumeOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f9182e35bd3c9badfbf82026615cc795b19604272986f7f66e2ef0aa74c4c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe32be4ea42618910ff747465a8c777d9225c75d2c8b5d1c3a16d01d22cd10e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093bf7c0e614ecfc83df6a4f5c6dfee5bf4971745d6c299660f1f49d562fc49b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecHosts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c144e3e27dbe34e2fa6ee57a9180e1b3b84cdf4acaf4b7f5e3d6929e257597b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaa0619e216c0a5a960f685523d044dd87805566ac4e545d91a586cb83fa218(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab23565463b427f6e3c44bd0b6b4cd4ab627e78404dd6efd050dc6e022511b4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecContainerSpecSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0d0e2ddfef0221c298bc9fe41f6045a46d8e23b5419ec7bf97a3646d269001(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7721b78fa9f7afc3125d860238ad2ce84651f22821b6676cca9e191dfc16e3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ead9d1c511fd77e747b7db69569f9e41e4848741782ee81ff52df2a32ef171f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb467d2da758c7805f59f6f0ba263404054286319f85c537827bd57a96a5755(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0b134416a24f542deef96ae47b50fe2b43ef67c898668977ae0658244b3679(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcac20ba0d2887683faa3ca7e10de92623cf5394d7b456ba4ae174be383b5675(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7734205260dd74d23fee5152abafc9b36182531d600d0b598154f6453042d7e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8c535cee67a662fea3dcf98056c4b9af400d456d0253919b366abf6485365b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe679b10020a7b55fc5ae722d748c1fd6d435dbbfc0cced01cce188699bbf99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3956831207ea96c857c976062daabd2f5da85bdbbe9ae115f26034de0c2471(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf0761ab1fb5115bdffe821513258858f43c75dd119cca25f9f6aa4e5530e24(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e9bff20a6fc7c32f4547c90197d03ec794c50257f636b35dcfa9d724b0c0dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e42dd8705d80516d52239e5bd5d2245867406818cb4b66c899de5a37c57d7bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512fd116e19432efb168a6081504e57386a7d8bc58a38f1dd4f2d878cb88a0f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f2ec641c8c2509957a126b12034e6156a5c507856e329be557a84d1a6a12af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c9e37912f628014316e53bdb6100003b3a8b006a3b12dd320d48a312749bc9(
    value: typing.Optional[ServiceTaskSpecContainerSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae949591f45fd69600eebc18b2bdfa82f7afc10d75a11fe7e033312183a29bfa(
    *,
    credential_spec: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    se_linux_context: typing.Optional[typing.Union[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__131e53e08fec9ae7579208f1125d438e44cde662e6dc2ca32214b6814e9bc1a2(
    *,
    file: typing.Optional[builtins.str] = None,
    registry: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c6e2ce95e6f52ad199db53df9e21fe0caa911a5ad47ee4d981bf95757f1600(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d652b2835b2a73b6ba16e1138af5d64b9b4062aefb2a29c27f77fe048a5230bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5677a35675011aa442d3ba6f1334f02630088e9e34db9df7ed8e0a5005c3b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9540a61e2632c9c8cc4659b0feec69bf1824ae4294ee79852e5b202616ca1b68(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesCredentialSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d4f2c5a7c78f0373dec2012f7ca9b8164f826283b9d34af07078d7e991e0b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e53a9201e38af527339a37e5bc82156047d072ba7c3d53103ef79477183b4cc(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivileges],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254d3b8aeac17082f30931cb771b0cc2344ecfcf7f36f33769dbd545d0823754(
    *,
    disable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    level: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2eb0fa88d491a35e234a830bdc6fa727fbdd09adab5c2bc9440200ac2f76b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debae7fc5aa795d8ac3f3e8a400fbfd945994824fdb6c68381cba782383ab0d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d02582404eb877613ea821680782f52cdf18a6a3b201a7e3ce5ec6c5e56c4f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4214d8ed502d438df21ec11a939ce0798eaa286a257df544a71fda200a23976(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864b1c74bed0bc8306b6251217653acb6c77c6078f1f652331f3c484911aa886(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccb625ae418999c22a801cfb154e07a6479ad6abed3413782da94f40f19cffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ff34c28c4a13282de02324672f4353d4cb93049797f2df37618e31a9b9b056(
    value: typing.Optional[ServiceTaskSpecContainerSpecPrivilegesSeLinuxContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f412006b7228b76c7c064fb5d2c28a3494a40fc5a6e3ecad65276c55deb4611b(
    *,
    file_name: builtins.str,
    secret_id: builtins.str,
    file_gid: typing.Optional[builtins.str] = None,
    file_mode: typing.Optional[jsii.Number] = None,
    file_uid: typing.Optional[builtins.str] = None,
    secret_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6128e489c639c5f5606ff02eb283b5aa2da9161f0ba58e4746c31781044fd6eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb68fbbedbfbf6d24de9ba07ee49488be184be18207d0cf0e1081b94e23343ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07442c58549902552cc6adeeac13e662313e3ea4ed6c55b5349ba7022c00d038(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c581da8e35de3b77fdcb545d0558e9fede5b8320f5fd3de6b053157ece0b9e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfaeb7b52d4c7494e6d122f3804f86dd9361cc9a9fca99762495fcca4a11a83e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1276d4afe39c3e6885b34a906dc1c716a0bd6b5ee97e13031567c1214fbadfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecContainerSpecSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d4a178db55677a5b428e859fad5b6d1072c614efc7775266a5049ea36fa01f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faa7ce39ef5aa42238dfb160040536b46569c58967e1221678ede2c36bb2ff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ef04d3872bf8057498985eaf9b53c50770e5ad93e7733bbbc39b43b7a9c38f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85a520180314087362957cbfad1031a8e0aa2dc8ddba903974de2aa6122546c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6711354182ba8d69c0c6f9f8f5298db4fec7d2dfdf574426ff7a1e18a2788da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66ddea3a9e039d8fa7a6925a69430e7d0933ef5e5d30e0c28fd6fe9be6c55c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441f32a325fdea7b03d43644550e2cdb0cf55413aec0d461abef229ade2fe6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300074047904645e1e6f2ad306100d1abc3e74b05e533b31f210c1849abb5334(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecContainerSpecSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbd929ea7551fb3075150c10da1eff5c5cda0f1cb8bc94922ea31a092ccd76d(
    *,
    name: builtins.str,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b5ac0eb8d0e43f156af2c575fd450f0479a24036f5da1281f211b9ab5b063c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b66ef38c5aaa07a2a1c0cceb5e6d0cedef8063e5a447b45f818bf0cff07392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa17f2d12944d0405d4bad4bca7320dd914e3190c5abdd5cf005c7cd353bae23(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b86d3e19445354139af150bfb4e374947e1ee460751f589f8e821b2591f7551(
    value: typing.Optional[ServiceTaskSpecLogDriver],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af86d732f02537efdfc19482334260392b85c88db9ac68421ef47b1fd802991(
    *,
    name: builtins.str,
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    driver_opts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1469f6a92ec6f955b8b6788209738f29fe58c9dd40955dd5be5ca383e66180e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25938098af537690526d615efeb48d98640e07d89cea50342ca91b4e0ac47d6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0a4223e84b2e57fe354f8591d50727c3411f016dafe5c75a026a39fef314e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b9c39d63a3a0115e9dfb3e5b6784e4cb9a31b985afc9b12b5c4413f79f712f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924afbe57660e7270b8cb1ea96e2d69a8ebb3ddcf67a886597a21ba0d4a5370e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69cb6fb1a065e24f82f3e9801d1c2750f4d863c711d54ca856c103975c0d5105(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecNetworksAdvanced]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed6b0df8dbe5294a16687cf58efe5ed8049234549331cbfc75230f23803e654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5e8264937b292c3379fd11041c63f2b5e43d1dfa4d9269cb8ae3b6a0869328(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304d3646766503fbcd231a5ff3ef4b34686a7cda39cb8217363a9d7f8c9238a3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc065d38a7e99fceb2d7c5d9d8e7a6b5dc567b4a2a4985c8f5f042684fcd110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5df6a34ac5dc480eafde4f9b8a9c674bf28d670dfe32dfccc7efec6ded892fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecNetworksAdvanced]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d1ad1fee972a0a4031a2d4070ff3bca4dcd07c596023e150fe3ae1eefaa1cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9757bf628f0655289ea2e0368b796904abdc5bb71d4db4d3cf407407c01bc53f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecNetworksAdvanced, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447b424e6883ffd5216c2e5613cdcc992af6ec661f12260fd5ae158c9db77982(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b1ffe6a3ae68e3e1a84ec54436bb17c6dfae0b74c1d77a34263078276fa229(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00496d30257bfce34cfa0457a148843c0f3097da9dbf6e89d038c96b886edb3d(
    value: typing.Optional[ServiceTaskSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c398e8317b8b76f3a50f9ff2b9b9d2b842459b191d14c3dc937276fcedc48fb(
    *,
    constraints: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_replicas: typing.Optional[jsii.Number] = None,
    platforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecPlacementPlatforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
    prefs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ef5e8aaf973fa907441962756fcdfcb7328fd489925e70924be6508da95a02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3c61857ee786a64a387dc4e7a197f6dfe72403da466aaf5c74ea70541622bb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceTaskSpecPlacementPlatforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171fc25f6bf060ea6f55313ea3241cd17894364fa33e146551c1b1ecd11f777d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab42f48513ad807ab4262f1887f4876130078dddbb7b09b1a8db445fcae53830(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a00072168fe4040b1497e66205f6822d42b6173d4f29d02c06b25383771f0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2da06140627ec70e45ca9872da6d469b6bc68ca6d7a3f03d826a8603b654a1(
    value: typing.Optional[ServiceTaskSpecPlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8d701e93fba0b5ef24907df3455ac2869963d6441556a916089ed878354744(
    *,
    architecture: builtins.str,
    os: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b23d9a6340cb053a9b697374f294be38c9539e67414237ed9f3a7eb6d7afe86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b40c62c539228e6c9663ebc5119f55b64430a1184d8c6c707ffa403b7bb15d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762f24acc0f058e61e9efe635276b8561cc4dadc0ca4b12d8ec51321d4574d58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffaeecd846e6479f4e10a4b1bf2062565e3c5f200ebc3aa7710da5abe9386751(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8470bd05dfed6f6fca0b8786ab4273ded46d935b6a7bfa5c0a6961fa0ac3edb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632e85caaa6b4d70ab66880f62e2792a4ce00ccbd7b9df2a5b3e082c15016da1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceTaskSpecPlacementPlatforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca81ad7b806a50f1be15acf57278677705f913f46421c9f38cc2291f2e3a3f80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208b2eec433f6f2a1735ab4240998c6dd576509a8170c7ca84554df16eef46f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb0b7c7023c94416c63227fbab2a29ad5ef955de218bf2ede9a34cfdd26496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa297aa6297ac4fdb14913ae6fb6297bff9228b0073d8ed37f485acf828b7237(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceTaskSpecPlacementPlatforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86e293b3f81a79db6ce44de0de5777883fe56e9f235f6240c895fb357afa5ec(
    *,
    limits: typing.Optional[typing.Union[ServiceTaskSpecResourcesLimits, typing.Dict[builtins.str, typing.Any]]] = None,
    reservation: typing.Optional[typing.Union[ServiceTaskSpecResourcesReservation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bfc372d64b112ac91ab5306dbdb7c310bf572a7de9613513fcc1e195ad57ce(
    *,
    memory_bytes: typing.Optional[jsii.Number] = None,
    nano_cpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad85cfb3bee08ea41923e289792e235c5dd24056db225f9885305ae601b6aab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ad4d720a8533f0b02cbb45cfda0c2fd6ea2afbdb3fd30e95bb7b605273216a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ed2b84f255a146752d4e124f45d9e82d9bef20b82b0e0b6785ef3a5d0ab764(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f567b2c4dd2b51bbc3b1cb5fa838946e0ecd547aeba4391a00055d34ae2fce3b(
    value: typing.Optional[ServiceTaskSpecResourcesLimits],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6504cc76ebe6f4dbc47c9ab4ec0f35710f4b8c142c3bb61a1e28065e263dfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be0dfddb64a6f3894d736c1ac32cd2d7dd7854322fed06cabae2bb527c96291(
    value: typing.Optional[ServiceTaskSpecResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d900f057607f5600beaed52b46c1f9a1486d6e09ed34cbaa6f81d85d3722c2e(
    *,
    generic_resources: typing.Optional[typing.Union[ServiceTaskSpecResourcesReservationGenericResources, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_bytes: typing.Optional[jsii.Number] = None,
    nano_cpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5419282a07d2a3da2ad843918d7477743d624f3cb1fbd894f57758dd95e45ffb(
    *,
    discrete_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
    named_resources_spec: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b37ddb1eb1bad0a948135c6df0d36392cf2148acaeb896c8ed6ea02d1acff43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29f33b0a408a567b9c8b1cc655a5e099d2cd9059cf524566bd378f7662bca83(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b56e9f6ad48e9f35635bd13369494820adf545132cd18c515b2841f78757ed5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97dbc1513607d1fa484b119089d7c2fb94cbcddcc6d47530f0f976db0420edcb(
    value: typing.Optional[ServiceTaskSpecResourcesReservationGenericResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7352e0aa5e0d0010647f0ef954963c21a3c8f5475aa064f1501e69692a81b650(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88df65653ba02379c74d09c7de8f18ace01eed3d29f6330da806ea4cddcb3f4c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98d9e8e12f0265c2e7dd0b37134a9d2a92320b4cc08303573fb273dbc8dca5ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc94289794034f6f8974e5bd10955364a48a10b11b4c37ac9e6090f9b587533(
    value: typing.Optional[ServiceTaskSpecResourcesReservation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7437c814147be937c1c47997767ede5a1b259cdc4e3b1e6e5e193c646de50fdf(
    *,
    condition: typing.Optional[builtins.str] = None,
    delay: typing.Optional[builtins.str] = None,
    max_attempts: typing.Optional[jsii.Number] = None,
    window: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70399785d868c8a7b63665143697f511a064ec8100a6a7d86365c420aa7fca0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60ccdd67452b44e4bdfd53e9dc23aeb4ce92d772359a2269eb5ed37c69083b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e109976de65f959aadfe4a17c35cd37fa9c9760877007c9734a74bbf02bd516d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522977757e9da66dfb31e8501d5bf874bfcf955a17de9b08ebc29cee6ef1b1dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e49fa6c7878e3ff73dda90dee88d248e428aea6c78c3051f6044db433f775c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a914df3ffe0d135d3dda47ccabe254795c23a121defc41c526c4b4acc718bac(
    value: typing.Optional[ServiceTaskSpecRestartPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c628a0c0d4e5e81f4dc17f6d7209e557d355883fbb98f565ffca41f75897c6e(
    *,
    delay: typing.Optional[builtins.str] = None,
    failure_action: typing.Optional[builtins.str] = None,
    max_failure_ratio: typing.Optional[builtins.str] = None,
    monitor: typing.Optional[builtins.str] = None,
    order: typing.Optional[builtins.str] = None,
    parallelism: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651035cce54779bae6d3163f6c82a70e7e92e9cee562a1eb904681286a3535c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b198f127a27702f5925fc4c0de0ce1aca9c67086ead8d25ede9b36fe7e9f182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d35840fb3b23d03a3e29cd67c8cf6031db6bb1693e4c9580239792055c7265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb374aafda9a7c530b8bc8d85434af22421b5fadeea36d9a262d93eedd9f880(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45af0fbbc8911944d2d77ea75e7a867a773adbf7255adc1373c8503a1341c974(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1624ea5554ed478103186b45adf1a9f59d4a708cbd16a4c1495f88a17f489322(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b10cf8ed743de0dd11eaaccd9b398a4a2f6e40798d0ec2f922ca3cd72ad59a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e6b5d77761966d099bff1406eda56313d90066dcc50bf5285f23a501f41879(
    value: typing.Optional[ServiceUpdateConfig],
) -> None:
    """Type checking stubs"""
    pass
