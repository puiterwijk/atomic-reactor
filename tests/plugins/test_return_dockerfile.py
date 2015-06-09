"""
Copyright (c) 2015 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""

from __future__ import unicode_literals

from dock.core import DockerTasker
from dock.inner import DockerBuildWorkflow
from dock.plugin import PreBuildPluginsRunner
from dock.plugins.pre_return_dockerfile import CpDockerfilePlugin
from dock.util import ImageName, DockerfileParser
from tests.constants import MOCK_SOURCE

class Y(object):
    pass

class X(object):
    image_id = "xxx"
    source = Y()
    source.dockerfile_path = None
    source.path = None
    base_image = ImageName(repo="qwe", tag="asd")

def test_returndockerfile_plugin(tmpdir):
    df_content = """
FROM fedora
RUN yum install -y python-django
CMD blabla"""
    df = DockerfileParser(str(tmpdir))
    df.content = df_content

    tasker = DockerTasker()
    workflow = DockerBuildWorkflow(MOCK_SOURCE, 'test-image')
    workflow.builder = X
    workflow.builder.df_path = df.dockerfile_path
    workflow.builder.df_dir = str(tmpdir)

    runner = PreBuildPluginsRunner(
        tasker,
        workflow,
        [{
            'name': CpDockerfilePlugin.key
        }]
    )
    runner.run()
    assert CpDockerfilePlugin.key is not None

    assert workflow.prebuild_results.get(CpDockerfilePlugin.key, "") == df_content