from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import users, courses, enrollments

app = FastAPI(
    title="EduTrack Lite API",
    description="A course enrollment and tracking system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/api/enrollments", tags=["Enrollments"])

@app.get("/")
def root():
    return {
        "message": "Welcome to EduTrack Lite API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)