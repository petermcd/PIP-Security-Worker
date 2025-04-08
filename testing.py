from xmlrpc.client import DateTime

from pip_security_worker.models.package import Package
from pip_security_worker.package_analysis.analyse import Analyse

package = Package(
    name='example',
    version='1.0.0',
    link='https://example.com',
    published=DateTime('2023-10-01T12:00:00Z'),
)

Analyse(package)
Analyse()
