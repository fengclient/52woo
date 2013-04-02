<?php
function PMA_getenv($envname)
{
   return $_SERVER[$envname];
}
function PMA_getIp()
{
    global $REMOTE_ADDR;
    global $HTTP_X_FORWARDED_FOR, $HTTP_X_FORWARDED, $HTTP_FORWARDED_FOR, $HTTP_FORWARDED;
    global $HTTP_VIA, $HTTP_X_COMING_FROM, $HTTP_COMING_FROM;

    // Get some server/environment variables values
    if (empty($REMOTE_ADDR) && PMA_getenv('REMOTE_ADDR')) {
        $REMOTE_ADDR = PMA_getenv('REMOTE_ADDR');
    }
    if (empty($HTTP_X_FORWARDED_FOR) && PMA_getenv('HTTP_X_FORWARDED_FOR')) {
        $HTTP_X_FORWARDED_FOR = PMA_getenv('HTTP_X_FORWARDED_FOR');
    }
    if (empty($HTTP_X_FORWARDED) && PMA_getenv('HTTP_X_FORWARDED')) {
        $HTTP_X_FORWARDED = PMA_getenv('HTTP_X_FORWARDED');
    }
    if (empty($HTTP_FORWARDED_FOR) && PMA_getenv('HTTP_FORWARDED_FOR')) {
        $HTTP_FORWARDED_FOR = PMA_getenv('HTTP_FORWARDED_FOR');
    }
    if (empty($HTTP_FORWARDED) && PMA_getenv('HTTP_FORWARDED')) {
        $HTTP_FORWARDED = PMA_getenv('HTTP_FORWARDED');
    }
    if (empty($HTTP_VIA) && PMA_getenv('HTTP_VIA')) {
        $HTTP_VIA = PMA_getenv('HTTP_VIA');
    }
    if (empty($HTTP_X_COMING_FROM) && PMA_getenv('HTTP_X_COMING_FROM')) {
        $HTTP_X_COMING_FROM = PMA_getenv('HTTP_X_COMING_FROM');
    }
    if (empty($HTTP_COMING_FROM) && PMA_getenv('HTTP_COMING_FROM')) {
        $HTTP_COMING_FROM = PMA_getenv('HTTP_COMING_FROM');
    }

    // Gets the default ip sent by the user
    if (!empty($REMOTE_ADDR)) {
        $direct_ip = $REMOTE_ADDR;
    }

    // Gets the proxy ip sent by the user
    $proxy_ip     = '';
    if (!empty($HTTP_X_FORWARDED_FOR)) {
        $proxy_ip = $HTTP_X_FORWARDED_FOR;
    } elseif (!empty($HTTP_X_FORWARDED)) {
        $proxy_ip = $HTTP_X_FORWARDED;
    } elseif (!empty($HTTP_FORWARDED_FOR)) {
        $proxy_ip = $HTTP_FORWARDED_FOR;
    } elseif (!empty($HTTP_FORWARDED)) {
        $proxy_ip = $HTTP_FORWARDED;
    } elseif (!empty($HTTP_VIA)) {
        $proxy_ip = $HTTP_VIA;
    } elseif (!empty($HTTP_X_COMING_FROM)) {
        $proxy_ip = $HTTP_X_COMING_FROM;
    } elseif (!empty($HTTP_COMING_FROM)) {
        $proxy_ip = $HTTP_COMING_FROM;
    } // end if... elseif...

    // Returns the true IP if it has been found, else false
    if (empty($proxy_ip)) {
        // True IP without proxy
        return $direct_ip;
    } else {
        $is_ip = preg_match('|^([0-9]{1,3}\.){3,3}[0-9]{1,3}|', $proxy_ip, $regs);
        if ($is_ip && (count($regs) > 0)) {
            // True IP behind a proxy
            return $regs[0];
        } else {
            // Can't define IP: there is a proxy but we don't have
            // information about the true IP
            return false;
        }
    } // end if... else...
} // end of the 'PMA_getIp()' function

echo PMA_getIp();