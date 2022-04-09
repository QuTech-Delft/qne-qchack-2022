# QuTech Quantum Network Explorer QKD Challenge

For QuTech's Quantum Network Explorer challenge your task is to implement one or
more Quantum Key Distribution (QKD) protocols and them make them robust to noisy
quantum channels. Your protocol must either produce a secure key at both Alice's
and Bob's locations or abort if an eavesdropper is detected. If you finish the
challenge early or would prefer to do something slightly different, you can also
address the open-ended part of the challenge related to authentication.

## Setting up

To set yourself up, you have two options, you can create the application
yourself and copy over the necessary template files, or you can copy over the
template and initialise the application instead.

### Create application yourself

First, create the application:

``` sh
qne application create qkd alice bob
```

and then copy over the necessary files from the template directory:

``` sh
cp template/src/app_alice.py template/src/app_bob.py template/src/epr_socket.py template/src/eve.py qkd/src
cp template/config/application.json qkd/config
```

This will ensure that your inputs and return values are consistent with what is
expected from the autograder.

### Copy the application template

Alternatively, you can simply copy the template directory

``` sh
cp -r template qkd
```

However, you still need to inform the CLI that the new directory is an
application by initialising it with:

``` sh
qne application init qkd
```

## NetQASM

### Documentation

Applications are written using the [NetQASM
SDK](https://github.com/QuTech-Delft/netqasm). For detailed documentation about
the available functionality, please see the [documentation
page](https://netqasm.readthedocs.io/en/latest/), and in particular
[netqasm.sdk](https://netqasm.readthedocs.io/en/latest/netqasm.sdk.html).

You may also want to read the paper introducing
[NetQASM](https://arxiv.org/abs/2111.09823).

### Note on EPR sockets

NetQASM uses EPR sockets to generate entangled pairs for use in applications.
The `netqasm.sdk` provides a suitable `EPRSocket` construct for this purpose.
However, for this challenge you MUST use the `EPRSocket` provided in the
`epr_socket.py` file. The `app_alice.py` and `app_bob.py` already have the
import correctly set up so just make sure you are not importing `EPRSocket` from
the `netqasm.sdk` as well.

This is done to enable the implementation of an eavesdropper who has control
over the entangled pair source. This is used by the autograder, but it is also
there for you to implement your own eavesdropper to test your protocol against!

### Note on generating multiple entangled pairs

You may be tempted to generate multiple entangled pairs in one go using
`epr_scoket.create_keep(n)`. However, the nodes used in the simulation do not
have very many qubits to hold these entangled states (as this is what the state
of the art is in labs). Instead, it is recommended that you generate one
entangled pair at a time and only generate the next one once the first one is
measured (thus releasing the qubit).

### Note on NetQASMConnection

Your code will use a `NetQASMConnection` object to communicate with the
simulator backend. In the provided application template the connection is
already set up for you and opened using a context manager `with alice:`/`with
bob:`. You must implement all your solution logic within that context and avoid
opening new contexts. Opening multiple connections is not currently supported.

### Note on debugging

This is the first time the QNE-ADK is being used for a public hackathon and as
such many features still need some time to mature. In particular, debugging
applications can be challenging at times. Here are some tips to help you with
debugging:
- Make sure you run experiments with your applications very often to ensure your
  code is runnable at all times and to make it easy to identify problematic
  code. The provided template will run without any errors so it provides a good
  starting point.
- In case of any issues, please make sure you have read the notes and check if
  any of them apply to your code.
- If an error happens in the simulator backend, the CLI may have to wait until
  the timeout expires (set with the `--timeout xx` option) before the experiment
  reports the failure. If your experiment seems to be running for longer than
  you expect, try cancelling it (e.g. with Ctrl-C) and then running it with a
  shorter timeout. However, if the application terminates due to a timeout
  without any additional error message then your application simply did not
  finish within the timeout and was terminated prematurely. This may mean that
  either the experiment itself may need a long time to run, e.g. if you are
  generating many entangled pairs, or you have an infinite loop somewhere.

## Tasks

The main goal of this challenge is to implement a QKD protocol that can generate
a secret key between Alice and Bob or abort if an eavesdropper is detected.

You will implement your application in the files `app_alice.py` and `app_bob.py`
which have already been setup for you with some skeleton code. You will use the
`EPRSocket` object to generate entangled pairs and `Socket` to send classical
messages between Alice and Bob. You can treat the classical communication
channel as if it were authenticated so you don't have to worry about
Man-in-the-Middle attacks. However, you should not make any such assumptions
about the entangled pair source.

Unless specified otherwise in the tasks below, your goal is to generate a secret
key between Alice and Bob or detect an eavesdropper. The key must be of length
`key_length` which is provided as an input parameter. Shorter and longer keys
will be rejected. The secret key must be a list consisting of integer 1's and
0's. Return the list as the value of the `secret_key` entry in the returned
dictionary. If an eavesdropper is detected, return `None` as the value of the
`secret_key`.

You can run `python autocheck.py` from the root of the repository to verify your
application. However, note that the provided `autocheck.py` does not check if
you correctly detect an eavesdropper. You are free to extend the `autocheck.py`
to also test for an eavesdropper. The autograder used on submission will test
for eavesdroppers.

## 1a. Basic protocols (easy)

The first step in the challenge is to implement one or more basic QKD protocols
in the absence of noise/losses on the quantum channel. That is, the produced
entangled pairs are perfect pure states.

Here are two protocols that you can implement using NetQASM in the provided ADK.
References are provided to the original publications in which that particular
protocol has been proposed, but you may find it useful to search for alternative
protocol explanations online (Google, YouTube, etc.).

- E91 (Ekert, Artur K. "Quantum Cryptography and Bell’s Theorem." Quantum
  Measurements in Optics. Springer, Boston, MA, 1992. 413-418.)
- BBM92 (Bennett, Charles H., Gilles Brassard, and N. David Mermin. "Quantum
  cryptography without Bell’s theorem." Physical review letters 68.5 (1992):
  557.)

Note that since the quantum networks we consider are built around distributing
entangled states rather than sending qubits BB84, which some of you may be
familiar with, is not on the list above. However, BBM92 is effectively an
entangled pair version of BB84. The paper referenced above for BBM92 proves this
equivalence.

The experiments are by default configured to not have any noise on the quantum
channels so you do not need any further configuration and can proceed to run
experiments as described in the [`README`](README.md) or run `autocheck.py`.

## 1b. Eavesdropper (optional)

So far there have been no eavesdroppers on your quantum channel so your QKD
protocol will have always produced a secret key. In this step you will implement
an eavesdropper and verify whether your protocol can correctly detect their
presence.

In your `qkd/src` directory you will have the file `eve.py`. In `eve.py` there
is the class `Eve` which you are free to implement as you wish. `Eve` receives
every entangled pair produced by the quantum channel through the method
`eavesdrop` to do with as you please. Your task is to implement an eavesdropping
strategy that can obtain as many bits of the secret key without being detected
by Alice and Bob.

You should then test if your protocol correctly detects an eavesdropper. Note
that the provided `autocheck.py` script will not do that for you. You may,
however, extend it to check for it as well.

Note that according to the QKD protocol security proofs you cannot succeed
against a correct implementation of such protocols. Please keep that in mind
when exploring eavesdropping strategies.

This task is optional. If you feel very confident with your QKD implementation
you can skip to the next task. Though please note, that your submission will be
tested against an eavesdropper.

## 2. Noisy qubits (difficult)

Now comes the real challenge. So far, you have been running your QKD protocol in
the absence of any noise on the quantum channel. This makes QKD very easy, but
unrealistic - there will always be some losses and errors. And then how do you
distinguish noise from an eavesdropper?

To explore the effect of noise on your QKD protocol, first make sure you have an
experiment created. In SquidASM simulations noise is introduced by setting the
fidelity of a channel to be less than `1.0` in the `experiment.json` file in the
experiment directory. If you are using the `randstad` network and haven't
changed any other settings, the channel you need to configure is the one
identified by the `slug` `amsterdam-leiden`.

Set the `value` of the `fidelity` parameter to `0.9` and run your experiment
again. This time, a protocol that assumes a noiseless channel should claim an
eavesdropper has been detected even if there wasn't one. If your implementation
still generates key, it is likely that you are comparing too few bits when
trying to check for the presence of an eavesdropper.

Your task is to now extend or reimplement QKD protocol to be able to distinguish
an eavesdropper from channel noise. This is done by adding [information
reconciliation and privacy
amplification](https://en.wikipedia.org/wiki/Quantum_key_distribution#Information_reconciliation_and_privacy_amplification)
phases to the QKD protocol. You can also find more information on this classical
post-processing phase in [this
paper](https://arxiv.org/abs/0910.0312)

In this task you must replace your initial simple reconciliation phase (in which
you most likely directly compared a select subset of bits of the raw key) with a
proper information reconciliation procedure in your QKD protocol such that you
can still produce a secret key in the presence of noise.

It is up to you to choose how you will implement information reconciliation. You
may design and implement it from scratch yourself or implement an existing
method that you find online. However, it is, quite clearly, important that you
do not perform this by simply revealing the entire key over the classical
channel.

Note that there is a theoretical threshold of noise below which it is no longer
possible to generate a secure secret key. Therefore, do not set the channel
fidelity to low. A value of `0.9` is reasonable for the purposes of this
challenge.

(Optional) You may, if you so wish, implement privacy amplification after you
have implemented information reconciliation. However, please disable it in your
submission as draws will be resolved based on which solution needed fewer
entangled pairs for a given length of key.

## Submission

Please ensure the following before submitting:
1. Your application is called `qkd` and your code is contained in
   `qkd/src/app_alice.py` and `qkd/src/app_bob.py`.
2. Your application takes the parameter `key_length` as input and returns a
   dictionary with single key-value pair with the key `secret_key`. The value
   should be either the secret key as a list of integer 1's and 0's or `None`.
3. Your application uses the `EPRSocket` class provided in the
   `qkd/src/epr_socket.py` file rather than from `netqasm.sdk`.

Once you have verified this, please upload your code to a location specified by
the organisers.

## Authentication (open-ended)

An important aspect in all QKD protocols is that the classical communication
channel used for all classical post-processing of the raw key material. However,
authentication requires secret key material. How do you then authenticate if you
cannot generate any secret key with QKD unless you already have some secret key?
In our simulations above we ignored this problem for the sake of convenience,
but it is a real challenge for practical deployments.

QKD protocols always need some initial key to perform the authentication which
is why they are sometimes called key extending protocols. There are a few ways
in which this can be done:
1. Provide some pre-shared secret key to the nodes which is the most secure, but
   also the most cumbersome method.
2. Use post-quantum cryptography for authentication which is less secure as it
   relies on the post-quantum algorithm being secure for the duration of the
   authentication, but more convenient as no pre-shared key is required.

Can you think of a better way with some better trade-off? If so, please include
an `authentication.md` file with your submission outlining your solution. You
can, of course, always implement a demonstration with your QKD protocol as well.
Submissions for this part of the challenge are not judged as part of the
hackathon. However, if your solution is particularly novel and interesting
QuTech may reach out to you for a more extensive discussion around your
proposal.
