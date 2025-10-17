using Microsoft.AspNetCore.Identity.UI.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Mail;
using System.Net.NetworkInformation;
using System.Threading.Tasks;
using SendGrid;
using SendGrid.Helpers.Mail;
using System;

namespace Terprint.Web.Services
{
    public class EmailSender : IEmailSender
    {
        public  Task SendEmailAsync(string email, string subject, string htmlMessage)
        {
            
                var apiKey = "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";
                var client = new SendGridClient(apiKey);
                var from = new EmailAddress("jgill@savitas.net", "Jamieson Gill");
                // var subject = "Sending with SendGrid is Fun";
                var to = new EmailAddress(email );
                var plainTextContent = htmlMessage;
                var htmlContent = htmlMessage;
                var msg = MailHelper.CreateSingleEmail(from, to, subject, plainTextContent, htmlContent);
                return client.SendEmailAsync(msg);
           
        }
    }
}
