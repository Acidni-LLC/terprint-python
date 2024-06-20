using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.HttpsPolicy;
//using Terprint_3.Pages;
//using Terprint_3.Components;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();
builder.Services.AddApplicationInsightsTelemetry(new Microsoft.ApplicationInsights.AspNetCore.Extensions.ApplicationInsightsServiceOptions
{
    ConnectionString = builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"]
});

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}
app.UseStaticFiles();

app.UseRouting();

app.UseAuthorization();
//app.UseMiddleware<Terprint_3.Pages.FilterChooser>();
app.MapRazorPages();
//app.MapRazorComponents<Terprint_3.Component.App>() ;

app.Run();