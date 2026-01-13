from setuptools import setup, find_packages

setup(
    name="langchian",
    version="0.2.5",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
        "streamlit",
        "requests",
        "pandas",
        "python-dotenv",
        "langchain",
        "langchain-core",
        "langchain-openai",
        "langchain-community",
        "openai",
        "faiss-cpu",
    ],
    description="Toy library for AI related stuff",
    author="",
)
