using Microsoft.AspNetCore.Components.Authorization;

namespace Terprint.Web.Services
{
    public class AuthService
    {
        private readonly AuthenticationStateProvider _authenticationStateProvider;

        public AuthService(AuthenticationStateProvider authenticationStateProvider)
        {
            _authenticationStateProvider = authenticationStateProvider;
        }

        public async Task<bool> IsAuthenticatedAsync()
        {
            var authState = await _authenticationStateProvider.GetAuthenticationStateAsync();
            return authState.User.Identity?.IsAuthenticated ?? false;
        }
    }
}