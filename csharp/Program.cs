using System;
using System.Security.Cryptography;
using System.Text;

class Program
{
    static void Main()
    {
        string claveSecreta = "yzbqklnj";
        Console.WriteLine(EncontrarNumeroAdventCoin(claveSecreta));
    }

    static int EncontrarNumeroAdventCoin(string claveSecreta)
    {
        using (MD5 md5 = MD5.Create())
        {
            int numero = 1;

            StringBuilder sb = new StringBuilder();

            while (true)
            {
                sb.Clear();
                sb.Append(claveSecreta+numero.ToString());

                byte[] entradaBytes = Encoding.UTF8.GetBytes(sb.ToString());
                byte[] hashBytes = md5.ComputeHash(entradaBytes);

                sb.Clear();

                for (int i = 0; i < hashBytes.Length; i++)
                {
                    sb.Append(hashBytes[i].ToString("x2"));
                }

                if (sb.ToString().StartsWith("000000"))
                {
                    return numero;
                }

                numero++;
            }
        }
    }
}