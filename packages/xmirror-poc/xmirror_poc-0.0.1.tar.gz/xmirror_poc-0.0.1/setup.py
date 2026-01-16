from setuptools import setup
with open("/tmp/poc.txt","w") as f: f.write("xmirror test!")
setup(
    name="xmirror-poc",
    version="0.0.1",
    description="poc test",
    author="test",
    author_email="test@gmail.com",
    license="MIT",
    packages=[],
)
