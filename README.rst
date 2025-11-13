Real time python package installation for Open edX
==================================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ that provides real time python package installation for Open edX platforms. This means you do not need to rebuild the openedx image whenever you add a new package. This is achieved by storing these packages in Django storage and downloading them inside each LMS/CMS container.

Installation
------------

This plugin depends on the `tutor-minio <https://github.com/overhangio/tutor-minio>`_ plugin to store the packages. After installing and enabling tutor-minio run the following commands:

``tutor plugins install livedeps``

``tutor plugins enable livedeps``

Then build the openedx image:

``tutor images build openedx``


Configuration
-------------

``LIVEDEPS`` (default: ``"[]"``)

To add a new package to this config run 

``tutor config save --append LIVEDEPS=package_name``

To remove an old package from this config run 

``tutor config save --remove LIVEDEPS=package_name``

Then run the following command to install the packages that are present in the ``LIVEDEPS`` config (make sure tutor is already running before executing this command):

``tutor local/k8s do livedeps``

You must wait 1 minute after running this command to see the changes reflected in the LMS/CMS.


Troubleshooting
---------------

This Tutor plugin is maintained by Muhammad Labeeb from `Edly <https://edly.io>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This work is licensed under the terms of the `GNU Affero General Public License (AGPL) <https://github.com/overhangio/tutor-minio/blob/release/LICENSE.txt>`_.