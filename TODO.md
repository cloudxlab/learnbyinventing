0. UX
    - the space is not working

1. Move the Line Fitting & Curve Fitting chapter to the begining
2. Introduce KNN and compare the line fitting with KNN
3. Gradient Descent

    In 'gradient_descent/slides.html#/1/1', after showing a function don't directly jump to 'Where is its minimum?'.

    Instead, do these:

    1. first ask them to plot it using desmos. I will put a screenshot of the same.
    2. Explain what is convex and Ask them whether this is a convex function or not.
    3. Ask them to write a python function to represent this function.
    4. Ask them to run that function at -5 and +5
    5. Now, ask them to do a hit and trial to figure out the value at which the function attains minimum. They can just use python notebook to call the function.
    6. Give them another convex function (x^2 -2x + 5) and ask them to find its minima manally. And then come up with a strategy.
    7. Now, let them convert their strategy into code. Do it by yourself. Show the function signature: 
        def find_minimum(x):
    ---
    1. Code a function is_minimum(x)?
    2. Code a function that return -1 if the function is decreasing at x, +1 if the function is increasing at x and 0 if it is not decreasing or increasing.
    3. change that function to return the how much is it increasing per increasing in x. It could be negative if the function is decreasing on increasing x.
    def diff(f, x):
        ....
    4. check diff(f, x=5) and diff(f, x=-5)
        Now, keep tweaking the value of x to bring the diff(f, x) to be zero. 
    5. Now, update your find_minima with using diff. if diff is positive reduce x else increase x. If the diff is very small, stop.
    6. Now, tweak your steps in a way, make a bigger jump if the diff is bigger in magntitude other wise make a smaller jump if diff is smaller.
    7. Print i, slope, f(x), x
    8. Try different values of properties
    

  
4. Give each chapter a unique identified  such - 1.1, 1.2, 2.1 etc. 
4. Decision Trees work log:
    * 