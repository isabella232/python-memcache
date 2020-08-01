# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.memcache_v1beta2.types import cloud_memcache
from google.longrunning import operations_pb2 as operations  # type: ignore

from .base import CloudMemcacheTransport
from .grpc import CloudMemcacheGrpcTransport


class CloudMemcacheGrpcAsyncIOTransport(CloudMemcacheTransport):
    """gRPC AsyncIO backend transport for CloudMemcache.

    Configures and manages Cloud Memorystore for Memcached instances.

    The ``memcache.googleapis.com`` service implements the Google Cloud
    Memorystore for Memcached API and defines the following resource
    model for managing Memorystore Memcached (also called Memcached
    below) instances:

    -  The service works with a collection of cloud projects, named:
       ``/projects/*``
    -  Each project has a collection of available locations, named:
       ``/locations/*``
    -  Each location has a collection of Memcached instances, named:
       ``/instances/*``
    -  As such, Memcached instances are resources of the form:
       ``/projects/{project_id}/locations/{location_id}/instances/{instance_id}``

    Note that location_id must be refering to a GCP ``region``; for
    example:

    -  ``projects/my-memcached-project/locations/us-central1/instances/my-memcached``

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "memcache.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "memcache.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
                quota_project_id=quota_project_id,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
            quota_project_id=quota_project_id,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def list_instances(
        self
    ) -> Callable[
        [cloud_memcache.ListInstancesRequest],
        Awaitable[cloud_memcache.ListInstancesResponse],
    ]:
        r"""Return a callable for the list instances method over gRPC.

        Lists Instances in a given project and location.

        Returns:
            Callable[[~.ListInstancesRequest],
                    Awaitable[~.ListInstancesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_instances" not in self._stubs:
            self._stubs["list_instances"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/ListInstances",
                request_serializer=cloud_memcache.ListInstancesRequest.serialize,
                response_deserializer=cloud_memcache.ListInstancesResponse.deserialize,
            )
        return self._stubs["list_instances"]

    @property
    def get_instance(
        self
    ) -> Callable[
        [cloud_memcache.GetInstanceRequest], Awaitable[cloud_memcache.Instance]
    ]:
        r"""Return a callable for the get instance method over gRPC.

        Gets details of a single Instance.

        Returns:
            Callable[[~.GetInstanceRequest],
                    Awaitable[~.Instance]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_instance" not in self._stubs:
            self._stubs["get_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/GetInstance",
                request_serializer=cloud_memcache.GetInstanceRequest.serialize,
                response_deserializer=cloud_memcache.Instance.deserialize,
            )
        return self._stubs["get_instance"]

    @property
    def create_instance(
        self
    ) -> Callable[
        [cloud_memcache.CreateInstanceRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the create instance method over gRPC.

        Creates a new Instance in a given project and
        location.

        Returns:
            Callable[[~.CreateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_instance" not in self._stubs:
            self._stubs["create_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/CreateInstance",
                request_serializer=cloud_memcache.CreateInstanceRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["create_instance"]

    @property
    def update_instance(
        self
    ) -> Callable[
        [cloud_memcache.UpdateInstanceRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the update instance method over gRPC.

        Updates an existing Instance in a given project and
        location.

        Returns:
            Callable[[~.UpdateInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_instance" not in self._stubs:
            self._stubs["update_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/UpdateInstance",
                request_serializer=cloud_memcache.UpdateInstanceRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["update_instance"]

    @property
    def update_parameters(
        self
    ) -> Callable[
        [cloud_memcache.UpdateParametersRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the update parameters method over gRPC.

        Updates the defined Memcached Parameters for an
        existing Instance. This method only stages the
        parameters, it must be followed by ApplyParameters to
        apply the parameters to nodes of the Memcached Instance.

        Returns:
            Callable[[~.UpdateParametersRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_parameters" not in self._stubs:
            self._stubs["update_parameters"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/UpdateParameters",
                request_serializer=cloud_memcache.UpdateParametersRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["update_parameters"]

    @property
    def delete_instance(
        self
    ) -> Callable[
        [cloud_memcache.DeleteInstanceRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the delete instance method over gRPC.

        Deletes a single Instance.

        Returns:
            Callable[[~.DeleteInstanceRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_instance" not in self._stubs:
            self._stubs["delete_instance"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/DeleteInstance",
                request_serializer=cloud_memcache.DeleteInstanceRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["delete_instance"]

    @property
    def apply_parameters(
        self
    ) -> Callable[
        [cloud_memcache.ApplyParametersRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the apply parameters method over gRPC.

        ApplyParameters will update current set of Parameters
        to the set of specified nodes of the Memcached Instance.

        Returns:
            Callable[[~.ApplyParametersRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "apply_parameters" not in self._stubs:
            self._stubs["apply_parameters"] = self.grpc_channel.unary_unary(
                "/google.cloud.memcache.v1beta2.CloudMemcache/ApplyParameters",
                request_serializer=cloud_memcache.ApplyParametersRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["apply_parameters"]


__all__ = ("CloudMemcacheGrpcAsyncIOTransport",)