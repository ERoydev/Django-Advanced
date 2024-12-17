import time

from django.utils.deprecation import MiddlewareMixin

# CUSTOM MIDDLEWARE CODE HERE

# Registriram go v settings
def measure_time_execution(get_response):
    def middleware(request, *args, **kwargs):
        start_time = time.time()
        response = get_response(request) # sledvashtoto neshto koeto shte se sluchi, executes next middleware or view
        end_time = time.time()

        print('Total time needed for execution with function ', end_time - start_time)

        return response

    return middleware


# class MeasureTimeExecution():
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     # Pravi go Callable(invokable) moga da izvikam instanciq ot tozi klass kato funkciq
#     def __call__(self, request, *args, **kwargs):
#         start_time = time.time()
#         response = self.get_response(request, *args, **kwargs)  # sledvashtoto neshto koeto shte se sluchi, executes next middleware or view
#         end_time = time.time()
#
#         print('Total time needed for execution with class ', end_time - start_time)
#
#         return response
#
#
#

class MeasureTimeExecution(MiddlewareMixin):

    def process_request(self, request):
        self.start_time = time.time()
        # return self.get_response() Tova vrushta poprincip po default

    def process_view(self, request, view, *args, **kwargs):
        print("Its processing...")

    def process_template_response(self, request, response):
        print('Its in the process template response')
        return response

    def process_response(self, request, response):
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        print(f"New class measure time: {total_time}")
        return response