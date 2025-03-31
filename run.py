import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.application.app:create_app",
        reload=True,
        factory=True,
        log_level="debug",
        use_colors=False,
    )
