using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;

namespace WinFormsExample
{
    public partial class Form1 : Form
    {
        private string ApiKey;
        private static readonly HttpClient httpClient = new HttpClient();

        public Form1()
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

        private async void btnLogin_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(ApiKey))
            {
                MessageBox.Show("API key is missing. Please ensure apikey.txt exists.");
                return;
            }

            // Validate input
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

            // Disable button during request
            btnLogin.Enabled = false;
            btnLogin.Text = "Logging in...";

            var payload = new
            {
                login = txtLogin.Text.Trim(),
                password = txtPassword.Text,
                q = ApiKey
            };

            try
            {
                var json = JsonConvert.SerializeObject(payload);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await httpClient.PostAsync("https://web-messenger-api-host.onrender.com/", content);

                if (response.IsSuccessStatusCode)
                {
                    var responseContent = await response.Content.ReadAsStringAsync();
                    MessageBox.Show("Login successful!");

                    // Clear password field for security
                    txtPassword.Clear();

                    // Here you can process the response and open main window
                    // For example, parse user data, tokens, etc.
                }
                else
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    MessageBox.Show($"Login failed: {response.ReasonPhrase}\nDetails: {errorContent}");
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
                btnLogin.Enabled = true;
                btnLogin.Text = "Log In";
            }
        }

        private void lblRegister_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            var registerForm = new RegisterForm();
            registerForm.ShowDialog();
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