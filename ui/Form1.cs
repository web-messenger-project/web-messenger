using System;
using System.Windows.Forms;

namespace LoginRegisterApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void lblRegister_Click(object sender, EventArgs e)
        {
            RegisterForm regForm = new RegisterForm();
            regForm.ShowDialog();
        }

        private void btnLogin_Click(object sender, EventArgs e)
        {
            string login = txtLogin.Text.Trim();
            string password = txtPassword.Text;

            if (string.IsNullOrEmpty(login) || string.IsNullOrEmpty(password))
            {
                MessageBox.Show("Please enter both login and password.", "Login Failed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (login == "admin" && password == "admin")
            {
                MessageBox.Show("Login successful!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                MessageBox.Show("Invalid login or password.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
