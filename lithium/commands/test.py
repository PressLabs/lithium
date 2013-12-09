import nose

from flask.ext.script import Command, Option

class TestCommand(Command):
  "Using nosetests, test them all!!!"

  def __init__(self, package, *args, **kwargs):
    super(TestCommand, self).__init__(*args, **kwargs)
    self.package = package

  option_list = (
    Option('--with-notify', '-wn', dest='notify'),
  )

  def run(self, notify):
    basic_nose_argv = ["tests=tests", "--with-coverage",
                       "--cover-package=%s" % self.package]

    nose.main(argv=basic_nose_argv)
