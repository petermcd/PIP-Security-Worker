"""Test for entry points."""

from pip_security_worker.cli import run_analysis, run_recent_updated_packages


class TestCli(object):
    """Test suite for entrypoints."""

    def test_run_analysis(self, mocker):
        """Test to ensure analysis is called."""
        analyze = mocker.patch('pip_security_worker.cli.Analyze')
        run_analysis()
        assert analyze.called

    def test_run_recent_updated_packages(self, mocker):
        """Test to ensure recent updated packages are fetched."""
        fetch_tasks = mocker.patch('pip_security_worker.cli.FetchTasks.update')
        run_recent_updated_packages()
        assert fetch_tasks.called
