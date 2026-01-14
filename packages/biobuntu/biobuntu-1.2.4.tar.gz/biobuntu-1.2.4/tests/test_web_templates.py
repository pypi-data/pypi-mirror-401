def test_web_templates_present():
    from importlib import resources

    web_pkg = resources.files("web")
    assert web_pkg.joinpath("templates", "index.html").is_file()
    # spot-check a static asset
    assert web_pkg.joinpath("static", "css", "style.css").is_file()
