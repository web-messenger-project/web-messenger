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
                ApiKey = File.ReadAllText(path).Trim();
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

            string login = txtLogin.Text;
            string password = txtPassword.Text;

            var payload = new
            {
                login,
                password,
                q = ApiKey
            };

            try
            {
                using (var client = new HttpClient())
                {
                    var json = JsonConvert.SerializeObject(payload);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    var response = await client.PostAsync("https://web-messenger-api-host.onrender.com/", content);

                    if (response.IsSuccessStatusCode)
                    {
                        MessageBox.Show("Login successful!");
                        
                    }
                    else
                    {
                        MessageBox.Show($"Login failed: {response.ReasonPhrase}");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error calling API: {ex.Message}");
            }
        }

        private void linkRegister_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            var registerForm = new RegisterForm();
            registerForm.ShowDialog();
        }
    }
}
