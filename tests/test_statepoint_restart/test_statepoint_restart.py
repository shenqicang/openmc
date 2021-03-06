#!/usr/bin/env python

import os
from subprocess import Popen, STDOUT, PIPE, call
import filecmp
import glob
from optparse import OptionParser

parser = OptionParser()
parser.add_option('--mpi_exec', dest='mpi_exec', default='')
parser.add_option('--mpi_np', dest='mpi_np', default='3')
parser.add_option('--exe', dest='exe')
(opts, args) = parser.parse_args()
cwd = os.getcwd()

def test_run():
    if opts.mpi_exec != '':
        proc = Popen([opts.mpi_exec, '-np', opts.mpi_np, opts.exe, cwd],
               stderr=STDOUT, stdout=PIPE)
    else:
        proc = Popen([opts.exe, cwd], stderr=STDOUT, stdout=PIPE)
    print(proc.communicate()[0])
    returncode = proc.returncode
    assert returncode == 0, 'OpenMC did not exit successfully.'

def test_created_statepoint():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    assert len(statepoint) == 1, 'Either multiple or no statepoint files exist.'
    assert statepoint[0].endswith('binary') or statepoint[0].endswith('h5'),\
        'Statepoint file is not a binary or hdf5 file.'

def test_results():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    call(['python', 'results.py', statepoint[0]])
    compare = filecmp.cmp('results_test.dat', 'results_true.dat')
    if not compare:
      os.rename('results_test.dat', 'results_error.dat')
    assert compare, 'Initial test results do not agree.'

def test_restart_form1():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    if opts.mpi_exec != '':
        proc = Popen([opts.mpi_exec, '-np', opts.mpi_np, opts.exe,
                      '-r', statepoint[0], cwd], stderr=STDOUT, stdout=PIPE)
    else:
        proc = Popen([opts.exe, '-r', statepoint[0], cwd], stderr=STDOUT, stdout=PIPE)
    print(proc.communicate()[0])
    returncode = proc.returncode
    assert returncode == 0, 'OpenMC restart 1 did not exit successfully.'

def test_created_statepoint_form1():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    assert len(statepoint) == 1, 'Either multiple or no statepoint files exist.'
    assert statepoint[0].endswith('binary') or statepoint[0].endswith('h5'),\
        'Statepoint file is not a binary or hdf5 file.'

def test_results_form1():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    call(['python', 'results.py', statepoint[0]])
    compare = filecmp.cmp('results_test.dat', 'results_true.dat')
    if not compare:
      os.rename('results_test.dat', 'results_error.dat')
    assert compare, 'Restart 1 test results do not agree.'

def test_restart_form2():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    if opts.mpi_exec != '':
        proc = Popen([opts.mpi_exec, '-np', opts.mpi_np, opts.exe,
                      '--restart', statepoint[0], cwd], stderr=STDOUT, stdout=PIPE)
    else:
        proc = Popen([opts.exe, '--restart', statepoint[0], cwd], stderr=STDOUT, stdout=PIPE)
    print(proc.communicate()[0])
    returncode = proc.returncode
    assert returncode == 0, 'OpenMC restart 2 did not exit successfully.'

def test_created_statepoint_form2():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    assert len(statepoint) == 1, 'Either multiple or no statepoint files exist.'
    assert statepoint[0].endswith('binary') or statepoint[0].endswith('h5'),\
        'Statepoint file is not a binary or hdf5 file.'

def test_results_form2():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    call(['python', 'results.py', statepoint[0]])
    compare = filecmp.cmp('results_test.dat', 'results_true.dat')
    if not compare:
      os.rename('results_test.dat', 'results_error.dat')
    assert compare, 'Restart 2 test results do not agree.'

def test_restart_serial():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    proc = Popen([opts.exe, '--restart', statepoint[0], cwd], stderr=STDOUT, stdout=PIPE)
    print(proc.communicate()[0])
    returncode = proc.returncode
    assert returncode == 0, 'OpenMC restart serial did not exit successfully.'

def test_created_statepoint_serial():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    assert len(statepoint) == 1, 'Either multiple or no statepoint files exist.'
    assert statepoint[0].endswith('binary') or statepoint[0].endswith('h5'),\
        'Statepoint file is not a binary or hdf5 file.'

def test_results_serial():
    statepoint = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    call(['python', 'results.py', statepoint[0]])
    compare = filecmp.cmp('results_test.dat', 'results_true.dat')
    if not compare:
      os.rename('results_test.dat', 'results_error.dat')
    assert compare, 'Restart serial test results do not agree.'

def teardown():
    output = glob.glob(os.path.join(cwd, 'statepoint.07.*'))
    output.append(os.path.join(cwd, 'results_test.dat'))
    for f in output:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':

    # test for openmc executable
    if opts.exe is None:
        raise Exception('Must specify OpenMC executable from command line with --exe.')

    # run tests
    try:
        test_run()
        test_created_statepoint()
        test_results()
        test_restart_form1()
        test_created_statepoint_form1()
        test_results_form1()
        test_restart_form2()
        test_created_statepoint_form2()
        test_results_form2()
        test_restart_serial()
        test_created_statepoint_serial()
        test_results_serial()
    finally:
        teardown()
