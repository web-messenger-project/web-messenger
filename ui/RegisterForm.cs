using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;

namespace WinFormsExample
{
    public partial class RegisterForm : Form
    {
        private string ApiKey;
        private static readonly HttpClient httpClient = new HttpClient();

        public RegisterForm()
        {
            InitializeComponent();
            LoadApiKey();
        }

        private void LoadApiKey()
        {
            try
            {
                string path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "apikey.txt");
                if (File.Exists(path))
                {
                    ApiKey = File.ReadAllText(path).Trim();
                }
                else
                {
                    MessageBox.Show("API key file not found. Please create apikey.txt in the application directory.");
                    ApiKey = null;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to load API key: {ex.Message}");
                ApiKey = null;
            }
        }

        private async void btnRegister_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(ApiKey))
            {
                MessageBox.Show("API key is missing. Please ensure apikey.txt exists.");
                return;
            }

            // Validate input
            if (string.IsNullOrWhiteSpace(txtName.Text))
            {
                MessageBox.Show("Please enter your name.");
                txtName.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtSurname.Text))
            {
                MessageBox.Show("Please enter your surname.");
                txtSurname.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtEmail.Text))
            {
                MessageBox.Show("Please enter your email.");
                txtEmail.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtLogin.Text))
            {
                MessageBox.Show("Please enter your login.");
                txtLogin.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtPassword.Text))
            {
                MessageBox.Show("Please enter your password.");
                txtPassword.Focus();
                return;
            }

            // Basic email validation
            if (!txtEmail.Text.Contains("@") || !txtEmail.Text.Contains("."))
            {
                MessageBox.Show("Please enter a valid email address.");
                txtEmail.Focus();
                return;
            }

            // Disable button during request
            btnRegister.Enabled = false;
            btnRegister.Text = "Registering...";

            var payload = new
            {
                name = txtName.Text.Trim(),
                surname = txtSurname.Text.Trim(),
                email = txtEmail.Text.Trim(),
                login = txtLogin.Text.Trim(),
                password = txtPassword.Text,
                q = ApiKey
            };

            try
            {
                string json = JsonConvert.SerializeObject(payload);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await httpClient.PostAsync("https://web-messenger-api-host.onrender.com/user/api/register/", content);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    MessageBox.Show("Registration successful! You can now log in.");
                    this.Close();
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    MessageBox.Show($"Registration failed: {response.ReasonPhrase}\nDetails: {errorContent}");
                }
            }
            catch (HttpRequestException ex)
            {
                MessageBox.Show($"Network error: {ex.Message}\nPlease check your internet connection.");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error calling API: {ex.Message}");
            }
            finally
            {
                // Re-enable button
                btnRegister.Enabled = true;
                btnRegister.Text = "Register";
            }
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                httpClient?.Dispose();
            }
            base.Dispose(disposing);
        }
    }
}