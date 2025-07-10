import { ref, onMounted, onUnmounted } from 'vue'
import { useAuth } from "@/composables/useAuth";
import { BACKEND_URL, TIMEOUT_ACCESS_TOKEN_CHECK } from '@/config';

const intervalId = ref<number | null>(null)

const startWatching = () => {
    if (intervalId.value !== null) return

    intervalId.value = setInterval(async () => {
      await watchAccessTokenValidity();
    }, TIMEOUT_ACCESS_TOKEN_CHECK);
  }

  const stopWatching = () => {
    if (intervalId.value !== null) {
      clearInterval(intervalId.value);
      intervalId.value = null;
    }
  }
  onMounted(() => startWatching());
  onUnmounted(() => stopWatching());

async function watchAccessTokenValidity(): Promise<void>{
    //retrieve access token
    const { isLoggedIn, token, refreshToken } = useAuth();

    if (isLoggedIn.value){

        //call an endpoint to check if access token must be updated
        const doUpdateAccessToken = await checkAccessToken(token.value!);

        //update access token if required
        if (!doUpdateAccessToken){
            return;
        }

        await updateAccessToken(refreshToken.value!);
    }
}

async function checkAccessToken(accessToken: string): Promise<boolean>{
    const updateAccessTokenRes = await fetch(`${BACKEND_URL}/auth/check_refresh_access_token`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        'Authorization': `Bearer ${accessToken}`
      },
    });

    if (!updateAccessTokenRes.ok) throw new Error(`Impossible de vérifier l'access token: ${updateAccessTokenRes.status}`);

    //retrieve boolean contained in response
    const doUpdateAccessToken = await updateAccessTokenRes.text();

    return doUpdateAccessToken ===  "true";
}

async function updateAccessToken(refreshToken: string): Promise<void>{
    //retrieve refresh token
    const response = await fetch(`${BACKEND_URL}/auth/refresh_access_token`, {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
        'Authorization': `Bearer ${refreshToken}`
         }
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(
        errorData.detail?.[0]?.msg || "Erreur lors du refresh de l'access token"
      );
    }

    const newAccessToken = await response.json();

    //save access token
    const { saveAccessToken } = useAuth();
    saveAccessToken(newAccessToken.access_token);
}

export { startWatching, stopWatching }