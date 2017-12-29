.. image:: Sew.png

Sew
===

Sew is a general purpose utility for working with threads in Python 3. With Sew, most boilerplate threading code is removed, allowing you to focus on the issue at hand. Most of Sew's functionality uses decorators. Here's an example of a threaded function:

.. code-block:: python

  import threading
  
  
  def foo(number):
      print("I'm running from a separate thread!")
      print("You passed me the number {}.".format(number))

  thread = threading.Thread(target=foo, args=(42,))
  thread.start()
  thread.join()
  
With Sew:
 
.. code-block:: python
 
  from sew import thread_join


  @thread_join
  def foo(number):
      print("I'm running from a separate thread!")
      print("You passed me the number {}.".format(number))

  foo(42)
  
Installing
----------

Sew is now on PyPi.org!

.. code-block:: shell

  pip install Sew
  
Or, in case ``pip3`` links to your local Python 3 installation:

.. code-block:: shell

  pip3 install Sew
  
Features
--------

Sew allows you to:

* Skip ``threading`` boilerplate code;
* Directly retrieve a threaded function's return value (blocking calls only);
* Easily call functions after a certain delay.

Objects
-------

Sew implements the following:

* ``thread`` (decorator): Call a function in a separate thread.

* ``thread_join`` (decorator): Call a function in a separate thread, and call ``thread.join()``.

* ``thread_daemon`` (decorator): Call a function in a separate daemon thread.

* ``thread_with_return_value`` (decorator): Call a function in a separate thread and return its return value.
  Note that this makes the function call a blocking operation.

|

* ``delay`` (decorator): Call a function after a certain delay.

* ``delay_join`` (decorator): Call a function after a certain delay, and join the thread.

* ``delay_daemon`` (decorator): Call a function after a certain delay, in a daemon thread.

* ``delay_with_return_value`` (decorator): Call a function after a certain delay and return its return value.
  Note that this makes the function call a blocking operation.

Examples
--------

* Reading from a ``list`` with a certain delay:

  .. code-block:: python
  
    from sew import delay_with_return_value

    numbers = [0, 1, 2, 3]


    @delay_with_return_value(0.5)
    def get_with_delay(index):
        """Wait half a second before returning numbers[index]."""
        return numbers[index]

    for index in range(4):
        print(get_with_delay(index))

* Waiting until a buffer is available for reading:

  .. code-block:: python
  
    import queue
    import time

    from sew import thread_join, thread


    buffer = ["Bar", "Foo"]
    queue = queue.Queue()


    @thread_join
    def wait_and_push():
        """Wait until the buffer is available, then put buffer.pop() into the queue."""
        time.sleep(1)
        # Simulate wait
        queue.put(buffer.pop())


    @thread
    def print_next():
        """Wait until a new element is available, then print it."""
        wait_and_push()
        print(queue.get(timeout=0.5))
        queue.task_done()

    print_next()
    print_next()
