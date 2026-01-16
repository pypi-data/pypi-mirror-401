from setuptools import setup, find_packages

setup(
    name="oscalling",
    version="1.0.0",
    author="Rheehose (Rhee Creative)",
    author_email="rheehose@example.com",
    description="A powerful OS manipulation package with built-in memory and hardware management.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rheehose/oscalling",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Intentionally keeping minimal dependencies for "speed" and "lightweight" claims,
        # but in a real scenario, psutil is standard for hardware logic.
        # I'll implement basic pure python fallbacks but list psutil as optional/recommended if I were strictly following best practices,
        # but for this specific request I'll add it if I decide to use it.
        # Let's try to stick to stdlib where possible to really prove "os module" power, 
        # but hardware stats usually need psutil.
        "psutil>=5.0.0" 
    ],
)
