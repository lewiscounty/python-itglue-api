import nox


@nox.session
def typecheck(session):
    session.install("mypy")
    session.run("mypy", "--strict", "-p", "itglue")


@nox.session(python=["3.7", "3.8", "3.9", "3.10"])
def test(session):
    session.install("coverage[toml]")
    session.run("coverage", "run", "--parallel-mode", "-m", "unittest", "discover")
    session.notify("coverage")


@nox.session
def coverage(session):
    session.install("coverage[toml]")
    session.run("coverage", "combine")
    session.run("coverage", "report", "-m")
