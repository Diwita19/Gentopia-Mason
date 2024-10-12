import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import openai
from typing import AnyStr, Optional, Type, Any
from gentopia.tools.basetool import BaseTool
load_dotenv()

openai.api_key = os.getenv('PUV2JH-V83G5G6WRG')


class MathAssistantArgs(BaseModel):
    query: str = Field(..., description="A math-related question or expression.")


class MathAssistant(BaseTool):
    """The tool provides assistance with various math-related questions and calculations."""

    name = "math_assistant"
    description = ("A tool to answer math calculations and questions. "
                   "Input should be a math-related question or expression.")

    args_schema: Optional[Type[BaseModel]] = MathAssistantArgs
    response_cache = {}

    def _is_math_question(self, query: AnyStr) -> bool:
        """To check if the query is related to math."""
        math_keywords = [
            # Geometry
            "area", "perimeter", "circumference", "volume", "triangle", 
            "circle", "square", "rectangle", "polygon", "ellipse", 
            "angle", "radius", "diameter", "height", "base", "length",
            "hypotenuse", "prism", "pyramid", "cone", "sphere", 
            "surface area", "solid", "congruence", "similarity", 
            "coordinate geometry", "shape", "geometric", "midpoint", 
            "slope", "distance", "tangent", "secant", "chord", 

            # Algebra
            "algebra", "expression", "equation", "inequality", 
            "variable", "constant", "function", "polynomial", 
            "factor", "expand", "simplify", "quadratic", 
            "linear", "exponential", "logarithm", "absolute value",
            "roots", "solutions", "system of equations", "substitution", 
            "elimination", "graph", "slope-intercept", "standard form",

            # Calculus
            "calculus", "derivative", "integral", "limit", 
            "continuity", "differentiation", "integration", 
            "fundamental theorem", "chain rule", "product rule", 
            "quotient rule", "definite integral", "indefinite integral", 
            "area under curve", "critical points", "inflection point", 
            "concavity", "optimization", "series", "sequences", 
            "Taylor series", "Riemann sum",

            # Statistics
            "statistics", "mean", "median", "mode", "variance", 
            "standard deviation", "distribution", "normal distribution", 
            "binomial distribution", "poisson distribution", "sample", 
            "population", "hypothesis testing", "confidence interval", 
            "p-value", "correlation", "regression", "ANOVA", 
            "chi-square", "data", "outlier", "frequency", 
            "quantile", "percentile", "interval", "random variable",

            # Foundational Maths
            "set theory", "logic", "proof", "combinatorics", 
            "graph theory", "number theory", "prime number", 
            "composite number", "factorial", "permutation", 
            "combination", "matrix", "vector", "determinant", 
            "transpose", "eigenvalue", "eigenvector", "linear algebra", 
            "Boolean algebra", "fractal", "calculus of variations", 
            "numerical analysis", "complex numbers", "imaginary unit", 
            "polar coordinates", "Cartesian coordinates"
        ]
        return any(keyword in query.lower() for keyword in math_keywords)

    def _run(self, query: AnyStr) -> str:
        if not self._is_math_question(query):
            return "I'm your math assistant! Please ask a question specifically related to math, and I'll do my best to assist you."

        # To check if response is cached
        if query in self.response_cache:
            return self.response_cache[query]

        try:
            # Call OpenAI's API
            response = openai.ChatCompletion.create(
                model='gpt-4',  # Use the latest available model
                messages=[{"role": "user", "content": query}],
                max_tokens=150  # Adjust as needed
            )
            answer = response['choices'][0]['message']['content'].strip()

            # Cached the response
            self.response_cache[query] = answer
            return answer
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    math_assistant = MathAssistant()
    # Single input prompt
    query = input("Ask a math question (or type 'exit' to quit): ")
    if query.lower() == 'exit':
        # Exit message
        print("Exiting the Math Assistant. Goodbye!")
    else:
        # Processing the query
        answer = math_assistant._run(query)
        # Print the answer
        print(answer)
