"""
Extended unit testing framework for OSG.

In order to meet the requirements of OSG testing, some extensions to the
standard Python unittest library have been made:
- additional test statuses 'OkSkip' and 'BadSkip'
"""
# quiet all the 'Method could be a function' or 'Invalid name' warnings;
# I'm following the conventions unittest set.
# pylint: disable=R0201,C0103
import sys
import unittest
import time


# Copied from unittest.util, Python 3.6
_MAX_LENGTH = 80
def safe_repr(obj, short=False):
    try:
        result = repr(obj)
    except Exception:
        result = object.__repr__(obj)
    if not short or len(result) < _MAX_LENGTH:
        return result
    return result[:_MAX_LENGTH] + ' [truncated]...'


# Define the classes we need to handle the two new types of test results: ok
# skip, and bad skip.

class OkSkipException(AssertionError):
    """
    This exception represents a test getting skipped for a benign reason,
    for example the component it is testing not being installed.
    """
    pass

class ExcludedException(AssertionError):
    """
    This exception represents a test getting excluded because it is not
    normally run for the given osg release series.
    """
    pass

class BadSkipException(AssertionError):
    """
    This exception represents a test getting skipped because success is
    impossible due to a previous error, for example a service that could
    not run.
    """
    pass

class TimeoutException(AssertionError):
    """
    This exceptions represents a test reaching a timeout described by
    the 'timeout' parameter of core._run_command()
    """
    pass


class OSGTestCase(unittest.TestCase):
    """
    A class whose instances are single test cases.
    An extension of unittest.TestCase with support for the 'OkSkip' and
    'BadSkip' statuses.

    See documentation for unittest.TestCase for usage.
    """

    # Needed to copy this from unittest so the private variable would work.
    def __init__(self, methodName='runTest'):
        """
        Create an instance of the class that will use the named test
        method when executed. Raises a ValueError if the instance does
        not have a method with the specified name.

        Usually, the user does not have to call this directly, but it will
        be called by unittest's test discovery functions instead.
        """
        unittest.TestCase.__init__(self, methodName)
        # in py2.4, testMethodName is a private variable, which means it has
        # a mangled version. Make a copy so methods we override can use it.

        # pylint:disable=E1101
        # Quiet error about missing member--I'm checking explicitly.
        if hasattr(self, '_TestCase__testMethodName'):
            self._testMethodName = self._TestCase__testMethodName

    def skip_ok(self, message=None):
        "Skip (ok) unconditionally"
        raise OkSkipException(message)

    def skip_ok_if(self, expr, message=None):
        "Skip (ok) if the expression is true"
        if expr:
            raise OkSkipException(message)

    def skip_ok_unless(self, expr, message=None):
        "Skip (ok) if the expression is false"
        if not expr:
            raise OkSkipException(message)

    def skip_bad(self, message=None):
        "Skip (bad) unconditionally"
        raise BadSkipException(message)

    def skip_bad_if(self, expr, message=None):
        "Skip (bad) if the expression is true"
        if expr:
            raise BadSkipException(message)

    def skip_bad_unless(self, expr, message=None):
        "Skip (bad) if the expression is false"
        if not expr:
            raise BadSkipException(message)

    def assertSubsetOf(self, a, b, message=None):
        "Ensure that a is a subset of b "
        if not set(a).issubset(set(b)):
            raise AssertionError(message)

    def failIfSubsetOf(self, a, b, message=None):
        "Ensure that a is not a subset of b"
        if set(a).issubset(set(b)):
            raise AssertionError(message)

    def assertEqualVerbose(self, actual, expected, message=None):
        aftermessage = "actual %s != expected %s" % (safe_repr(actual), safe_repr(expected))
        if message:
            fullmessage = "%s (%s)" % (message, aftermessage)
        else:
            fullmessage = aftermessage
        self.assertEqual(actual, expected, fullmessage)

    # This is mostly a copy of the method from unittest in python 2.4.
    # There is some code here to test if the 'result' object accepts 'skips',
    # since the original TestResult object does not. If it does not, an
    # okSkip is considered a success, and a badSkip is considered a failure
    # (or an error if it happens in setUp).
    def run(self, result=None, **kwargs):
        """
        Run a single test method. Catch any Exceptions the method raises
        and count them as Errors, Failures, OkSkips, or BadSkips depending
        on the exception class.

        Results are counted in a TestResult instance, 'result'. If result
        contains support for skips (which an OSGTestResult instance does),
        then OkSkipExceptions and BadSkipExceptions are counted appropriately.
        If not, an OkSkipException is counted as a success, and a
        BadSkipException is counted as an Error or a Failure depending on when
        it occurs.
        """
        exit_on_fail = False
        if 'exit_on_fail' in kwargs:
            exit_on_fail = kwargs['exit_on_fail']

        if result is None:
            result = self.defaultTestResult()
        result.startTest(self)
        testMethod = getattr(self, self._testMethodName)
        canSkip = hasattr(result, 'addOkSkip') and hasattr(result, 'addBadSkip')
        try:
            try:
                self.setUp()
            # These are new. setUp() is a perfectly valid place to skip tests.
            except OkSkipException:
                if canSkip:
                    result.addOkSkip(self, sys.exc_info())
                else:
                    pass
                return
            except ExcludedException:
                if canSkip:
                    result.addExclude(self, sys.exc_info())
                else:
                    pass
                return
            except BadSkipException:
                if canSkip:
                    result.addBadSkip(self, sys.exc_info())
                else:
                    result.addError(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
                return
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
                return

            ok = False
            try:
                testMethod()
                ok = True
            # Add support for the new exception classes.  These need to be
            # _before_ self.failureException, since self.failureException is
            # another name for AssertionError, and OkSkipException and
            # BadSkipException inherit from AssertionError.
            except OkSkipException:
                if canSkip:
                    result.addOkSkip(self, sys.exc_info())
                else:
                    pass
            except ExcludedException:
                if canSkip:
                    result.addExclude(self, sys.exc_info())
                else:
                    pass
            except BadSkipException:
                if canSkip:
                    result.addBadSkip(self, sys.exc_info())
                else:
                    result.addFailure(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
            except TimeoutException:
                result.addTimeout(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
            except self.failureException:
                result.addFailure(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()

            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, sys.exc_info())
                if exit_on_fail:
                    result.stop()
                ok = False
            if ok:
                result.addSuccess(self)
        finally:
            result.stopTest(self)

    def __str__(self):
        module = self.__class__.__module__
        if '.' in module:
            module = module[module.rfind('.')+1:]  # strip off all but the last component
        return "%s.py: %s" % (module, self._testMethodName)


class OSGTestResult(unittest.TestResult):
    """
    Extended holder of test result information.

    Like unittest.TestResult, it does not need to be manipulated by test
    writers. In addition to what's in TestResult, each instance also holds
    collections of skipped tests, separated according to whether or not the
    skip was "bad". The collections contain (testcase, exceptioninfo) tuples,
    where exceptioninfo is a formatted traceback, and testcase is the actual
    OSGTestCase object.
    """

    def __init__(self):
        unittest.TestResult.__init__(self)
        self.okSkips = []
        self.badSkips = []
        self.excludes = []
        self.timeouts = []

    def addOkSkip(self, test, err):
        """Called when an ok skip has occurred. 'err' is a tuple as returned by sys.exc_info()"""
        self.okSkips.append((test, self.osg_exc_info_to_string(err, test)))

    def addExclude(self, test, err):
        """Called when a test is excluded. 'err' is a tuple as returned by sys.exc_info()"""
        self.excludes.append((test, self.osg_exc_info_to_string(err, test)))

    def addBadSkip(self, test, err):
        """Called when a bad skip has occurred. 'err' is a tuple as returned by sys.exc_info()"""
        self.badSkips.append((test, self.osg_exc_info_to_string(err, test)))

    def addTimeout(self, test, err):
        """Called when a timeout has occurred. 'err' is a tuple as returned by sys.exc_info()"""
        self.timeouts.append((test, self.osg_exc_info_to_string(err, test)))

    def osg_exc_info_to_string(self, err, test):
        """Get the string description out of an Ok/BadSkipException.
        Pass it up to the parent if the exception is not one of those.
        """
        exctype, value, _ = err

        if exctype in (OkSkipException, ExcludedException, BadSkipException, TimeoutException):
            return str(value)
            # TODO Need some way to print out the line that caused the skip
            # if there is no message.
            # This requires using the traceback module and filtering out
            # stack frames we don't care about.
            #return traceback.format_tb(tb)[-1] + ' ' + ''.join(traceback.format_exception_only(exctype, value))
        else:
            return self._exc_info_to_string(err, test)

    def wasSuccessful(self):
        """Tells whether or not this result was a success, considering bad skips as well."""
        return len(self.failures) == len(self.errors) == len(self.badSkips) == len(self.timeouts) == 0

    def wasPerfect(self):
        """Tells whether or not this result was perfect, i.e. successful and without any skips."""
        return self.wasSuccessful() and len(self.okSkips) == 0

    def __repr__(self):
        cls = self.__class__
        return "<%s.%s run=%d errors=%d failures=%d okSkips=%d badSkips=%d timeouts=%d>" % (
            cls.__module__,
            cls.__name__,
            self.testsRun,
            len(self.errors),
            len(self.failures),
            len(self.okSkips),
            len(self.badSkips),
            len(self.timeouts))


class OSGTextTestResult(OSGTestResult):
    """
    A test result that formats results and prints them to a stream.

    Used by OSGTextTestRunner.
    This is copied from unittest._TextTestResult instead of subclassing it
    since that's a private interface (and is not called the same thing in py2.6).

    The user should not have to instantiate this directly; an instance will be
    created by OSGTextTestRunner.
    """

    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        OSGTestResult.__init__(self)
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)

    def startTest(self, test):
        OSGTestResult.startTest(self, test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")

    def addSuccess(self, test):
        OSGTestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            self.stream.write('.')

    def addError(self, test, err):
        OSGTestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')

    def addFailure(self, test, err):
        OSGTestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')

    def printErrors(self):
        """Print a list of errors, failures and skips to the stream."""
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)
        self.printErrorList('TIMEOUT', self.timeouts)
        self.printSkipList('BAD SKIPS', self.badSkips)
        self.printSkipList('OK SKIPS', self.okSkips)
        self.printSkipList('EXCLUDED', self.excludes)

    def printErrorList(self, flavour, errors):
        """Print all of one flavor of error to the stream."""
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln(str(err))

    def printSkipList(self, flavour, skips):
        """Print all of one flavor of skip to the stream."""
        if not skips:
            return

        self.stream.writeln(self.separator1)
        self.stream.writeln("%s:" % flavour)
        self.stream.writeln(self.separator2)
        for test, skip in skips:
            self.stream.writeln("%s %s" % (self.getDescription(test), str(skip)))
        self.stream.writeln("")

    def addOkSkip(self, test, reason):
        OSGTestResult.addOkSkip(self, test, reason)
        if self.showAll:
            self.stream.writeln("okskip")
        elif self.dots:
            self.stream.write("s")

    def addExclude(self, test, reason):
        OSGTestResult.addExclude(self, test, reason)
        if self.showAll:
            self.stream.writeln("excluded")
        elif self.dots:
            self.stream.write("x")

    def addBadSkip(self, test, reason):
        OSGTestResult.addBadSkip(self, test, reason)
        if self.showAll:
            self.stream.writeln("BADSKIP")
        elif self.dots:
            self.stream.write("S")

    def addTimeout(self, test, reason):
        OSGTestResult.addTimeout(self, test, reason)
        if self.showAll:
            self.stream.writeln("TIMEOUT")
        elif self.dots:
            self.stream.write("F")

class OSGTextTestRunner(unittest.TextTestRunner):
    """Extended unittest.TextTestRunner with support for okSkips / badSkips / timeouts."""

    def _makeResult(self):
        return OSGTextTestResult(self.stream, self.descriptions, self.verbosity)

    def run(self, test, **kwargs):
        """
        Run an actual set of tests, time the run, collect and
        summarize the results.

        This is an extended version of unittest.TextTestRunner.run() which
        displays okSkips, badSkips, and timeouts.
        """
        result = self._makeResult()
        # ^ make 'result' here so we know its an OSGTextTestResult and not a
        #   regular TextTestResult.
        startTime = time.time()
        test(result, **kwargs)
        stopTime = time.time()
        timeTaken = stopTime - startTime
        result.printErrors()
        self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()
        if not result.wasSuccessful():
            failed, errored, badSkipped, timeouts, okSkipped = map(len,
                (result.failures, result.errors, result.badSkips, result.timeouts, result.okSkips))
            counts = []
            if failed:
                counts.append("failures=%d" % failed)
            if errored:
                counts.append("errors=%d" % errored)
            if badSkipped:
                counts.append("badSkips=%d" % badSkipped)
            if timeouts:
                counts.append("timeouts=%d" % timeouts)
            if okSkipped:
                counts.append("okSkips=%d" % okSkipped)
            self.stream.writeln("FAILED (" + ", ".join(counts) + ")")
        else:
            self.stream.write("OK")
            if not result.wasPerfect():
                self.stream.write("(okSkips=%d)" % len(result.okSkips))
            self.stream.write("\n")
        return result

class OSGTestSuite(unittest.TestSuite):
    """
    An extended version of unittest.TestSuite that passes arbitrary keyword args
    onto the test cases
    """
    def run(self, result, **kwargs):
        for test in self._tests:
            if result.shouldStop:
                break
            test(result, **kwargs)
        return result

class OSGTestLoader(unittest.TestLoader):
    """
    An extended version of unittest.TestSuite that creates OSG Test Suites
    when loading tests
    """
    suiteClass = OSGTestSuite
