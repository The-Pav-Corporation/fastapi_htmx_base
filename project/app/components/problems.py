from ..schemas.problem import Problem 

def problem_list_view(title: str, description: str, id: int):
    return f"""
        <div class="card" style="width: 18rem; margin: 10px;">
            <div class="card-body">
                <h5 class="card-title">{title}</h5>
                <div style="max-height: 9rem; overflow: hidden; white-space: no-wrap; margin-bottom: 5px;">
                    <p class="card-text">{description}</p>
                </div>
                <a href="#problems/{id}"
                    hx-get="/problems/{id}"
                    hx-trigger="click"
                    hx-target="#content"
                    class="btn btn-primary">Details</a>
                <a href="#problems/"
                    hx-get="/problems/{id}/delete"
                    hx-trigger="click"
                    hx-target="#content"
                    class="btn btn-danger">Delete</a> 
                    </div>
        </div>
        """

def problem_create_view():
    return """
    <form action="/problems/" method="POST">
        <div class="mb-3 row">
            <label for="problem_title" class="col-sm-1 col-form-label">Title</label>
            <div class="col-sm-11">
                <input type="text" name="title" class="form-control" id="problem_title" placeholder="The title of the problem">
            </div>
        </div>
        <div class="mb-3 row">
            <label for="problem_description" class="col-sm-1 col-form-label">Description</label>
            <div class="col-sm-11">
                <textarea name="description" id="problem_description" cols="137" rows="10"></textarea>
                <!-- <input type="text" class="form-control" id="problem_description" placeholder="The description of the problem"> -->
            </div>
        </div>
        <input type="submit" value="Create" class="btn btn-primary mb-3">
    </form>
    """

def problem_detail_view(problem: Problem):
    solved = "Solved" if problem.is_solved else "Not Solved"
    solution = '<p id="solution">Solution: {problem.solution}</p>' if problem.solution else ''
    return f"""
    <h2>{problem.title}</h2>
    <div class="container">
        <p>{problem.description}</p>
        <p>{solved}</p>
        <form action="/problems/{problem.id}/solve" method="POST">
            <div class="mb-3 row col-sm-5">
                <label for="problem_input" class="col-sm-1 col-form-label">Input</label>
                <div class="col-sm-11">
                    <input type="text" name="problem_input" class="form-control col-sm-4" id="problem_input" placeholder="Dataset">
                </div>
            </div>
        <input type="submit" value="Get Solution" class="btn btn-primary mb-3">
        </form>
        {solution}
        <a href="#problems/"
            hx-get="/problems/{problem.id}/delete"
            hx-trigger="click"
            hx-target="#content"
            class="btn btn-danger">Delete</a> 
    </div>

    """