import panel as pn
pn.extension()
from panel.widgets.input import PasswordInput
password_input = pn.widgets.input.PasswordInput(name='Password', placeholder='Enter the password that you would like to use...')
password_input

#password_input.value