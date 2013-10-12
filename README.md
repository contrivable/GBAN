GBAN
====

German Bank Account Numbers

The main concern of this project is to research and implement checking methods for German bank account number. There are currently about 150 checking methods with a lot of them adapting previously existing methods and/or chaining them together.
The most common idea seems to be to add a weighted part of the account number as it is given on bank cards and compare the further recalculated sum against one digit in the account number.
One problem here is that methods generally expect 10 digits in an account number but do not explain how to deal with shorter numbers - outside specification it seems agreed upon to simple prepend zeros (add to the left side) until 10 digits are reached.
Methods seem to have a different understanding of what the account number is, i.e. which digits belong to the calculation base. Besides the account digits there is mainly the check digit but also so-called working digits or sub-account digits which are used in some methods and not used in others.

Early goals here are:
* explain where resources and quarterly updates about checking methods can be found
* explain how to extract bank information from different resources
* translate German description of checking methods into English with priority on content
* translate descriptions of checking methods to like pseudo code
* implement all checking methods
* * somewhat repetitive and boring so it will take some time, expect 10 methods a day

Late goals:
* implement some way of getting updates from the German Federal Bank in a timely fashion
* implement BIC and IBAN search
* implement some variant of reverse account number
* * specifying missing digits may result in provision of possible combinations there

20131012
