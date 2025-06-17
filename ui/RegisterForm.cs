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
                ApiKey = File.ReadAllText(path).Trim();
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

            string name = txtName.Text;
            string surname = txtSurname.Text;
            string email = txtEmail.Text;
            string login = txtLogin.Text;
            string password = txtPassword.Text;

            var payload = new
            {
                name,
                surname,
                email,
                login,
                password,
                q = ApiKey
            };

            try
            {
                using (var client = new HttpClient())
                {
                    string json = JsonConvert.SerializeObject(payload);
                    var content = new StringContent(json, Encoding.UTF8, "application/json");

                    var response = await client.PostAsync("https://yourapi.com/register", content);

                    if (response.IsSuccessStatusCode)
                    {
                        MessageBox.Show("Registration successful!");
                        this.Close();
                    }
                    else
                    {
                        MessageBox.Show($"Registration failed: {response.ReasonPhrase}");
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error calling API: {ex.Message}");
            }
        }
    }
}
