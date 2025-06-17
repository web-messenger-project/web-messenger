using System;
using System.Windows.Forms;

namespace LoginRegisterApp
{
    public partial class RegisterForm : Form
    {
        public RegisterForm()
        {
            InitializeComponent();
        }

        private void btnRegister_Click(object sender, EventArgs e)
        {
            string info = $"Name: {txtName.Text}\n" +
                          $"Surname: {txtSurname.Text}\n" +
                          $"Email: {txtEmail.Text}\n" +
                          $"Login: {txtLogin.Text}\n" +
                          $"Password: {txtPassword.Text}";

            MessageBox.Show(info, "Registered Info", MessageBoxButtons.OK, MessageBoxIcon.Information);

            this.Close();
        }
    }
}
