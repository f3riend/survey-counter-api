from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns
import base64
import logging

# Pydantic models
class Question(BaseModel):
    question: str = Field(..., description="Question text")
    answers: List[str] = Field(..., description="List of possible answers")
    response: List[str] = Field(..., description="List of given responses")

class SurveyData(BaseModel):
    questions: List[Question] = Field(..., description="List of questions")

class PlotResponse(BaseModel):
    plots: List[str] = Field(..., description="List of plots in base64 format")
    success: bool = Field(True, description="Operation success status")
    message: str = Field("Plots created successfully", description="Status message")

# FastAPI application
app = FastAPI(
    title="Survey Analysis API",
    description="API for analyzing and visualizing survey data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def count_responses(question: Question) -> Dict[str, int]:
    """
    Count responses for a question and sort in descending order.
    
    Args:
        question: Question model
        
    Returns:
        Dict[str, int]: Answer-count mapping
    """
    try:
        responses = question.response
        answer_count = {answer: responses.count(answer) for answer in question.answers}
        sorted_answers = sorted(answer_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_answers)
    except Exception as e:
        logger.error(f"Error counting responses: {e}")
        raise HTTPException(status_code=400, detail=f"Error counting responses: {str(e)}")

def plot_to_base64(question: Question) -> str:
    """
    Create a bar plot for the question and convert to base64 string.
    
    Args:
        question: Question model
        
    Returns:
        str: Plot in base64 format
    """
    try:
        responses = count_responses(question)
        
        if not responses:
            raise ValueError("Insufficient data to create plot")
        
        # Plot settings
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")
        
        # Create bar plot
        ax = sns.barplot(
            x=list(responses.values()), 
            y=list(responses.keys()), 
            palette='viridis'
        )
        
        # Customize plot
        plt.title(question.question, fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Number of Responses', fontsize=12)
        plt.ylabel('Answers', fontsize=12)
        
        # Show values on bars
        for i, v in enumerate(responses.values()):
            ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_base64
        
    except Exception as e:
        logger.error(f"Error creating plot: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating plot: {str(e)}")

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "message": "Survey Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "/analyze (POST)"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/analyze", response_model=PlotResponse, tags=["Analysis"])
async def analyze_survey(survey_data: SurveyData):
    """
    Analyze survey data and create visualizations.
    
    Args:
        survey_data: Survey data
        
    Returns:
        PlotResponse: Plots in base64 format
    """
    try:
        if not survey_data.questions:
            raise HTTPException(status_code=400, detail="At least one question is required")
        
        plot_list = []
        
        for i, question in enumerate(survey_data.questions):
            logger.info(f"Processing question {i+1}: {question.question}")
            
            # Data validation
            if not question.response:
                logger.warning(f"No responses found for question {i+1}")
                continue
                
            # Filter invalid responses
            valid_responses = [r for r in question.response if r in question.answers]
            if len(valid_responses) != len(question.response):
                logger.warning(f"Some invalid responses filtered for question {i+1}")
                question.response = valid_responses
            
            if valid_responses:
                plot_base64 = plot_to_base64(question)
                plot_list.append(plot_base64)
        
        if not plot_list:
            raise HTTPException(status_code=400, detail="No plots could be created")
        
        logger.info(f"Created {len(plot_list)} plots successfully")
        
        return PlotResponse(
            plots=plot_list,
            success=True,
            message=f"{len(plot_list)} plots created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"General error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Run application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)