<?php

namespace OCA\RDS\Controller;

require __DIR__ . '/../../vendor/autoload.php';

use phpseclib3\Crypt\RSA;
use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\Util;
use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};

use \Firebase\JWT\JWT;

/**
- Define a new page controller
 */

class PageController extends Controller
{
    protected $appName;
    private $userId;

    /**
     * @var IURLGenerator
     */
    private $urlGenerator;

    /**
     * @var UrlService
     */
    private $urlService;

    private $rdsService;

    private $public_key;
    private $private_key;

    use Errors;


    public function __construct(
        $AppName,
        IRequest $request,
        $userId,
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        RDSService $rdsService
    ) {
        parent::__construct($AppName, $request);
        $this->appName = $AppName;
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();

        $config = array(
            "digest_alg" => "sha512",
            "private_key_bits" => 1024,
            "private_key_type" => OPENSSL_KEYTYPE_RSA,
        );

        $private_key_res = openssl_pkey_new($config);
        openssl_pkey_export($private_key_res, $this->private_key);
        $this->public_key = openssl_pkey_get_details($private_key_res)['key'];


        $private = RSA::createKey();
        $this->private = $private->withPadding(RSA::SIGNATURE_PKCS1);
        $this->public = $private->getPublicKey();
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */
    public function index()
    {
        $policy = new \OCP\AppFramework\Http\EmptyContentSecurityPolicy();
        $policy->addAllowedConnectDomain(parse_url($this->urlService->getURL())["host"]);
        $policy->addAllowedConnectDomain("http://localhost:8080");
        $policy->addAllowedConnectDomain("ws://localhost:8080");
        \OC::$server->getContentSecurityPolicyManager()->addDefaultPolicy($policy);

        $userId = $this->userSession->getUser()->getUID();

        $params = [
            'clients' => $this->clientMapper->findByUser($userId),
            'user_id' => $userId,
            'urlGenerator' => $this->urlGenerator,
            "cloudURL" => $this->urlService->getURL(),
            "oauthname" => $this->rdsService->getOauthValue(),
        ];

        return new TemplateResponse('rds', "main.research", $params);
    }

    /**
     * Returns the user mail address
     *
     * @return object an object mailaddress
     *
     * @NoAdminRequired
     * @NoCSRFRequired
     */
    public function mailaddress()
    {
        return $this->handleNotFound(function () {
            $user = \OC::$server->getUserSession()->getUser();
            $data = [
                "email" => $user->getEMailAddress(),
                "username" => $user->getUserName(),
                "displayname" => $user->getDisplayName()
            ];

            $jwt = JWT::encode($data, $this->private_key, 'RS256');
            return $jwt;
        });
    }

    /**
     * Returns the public key for mailadress
     *
     * @return object an object with publickey
     *
     * @PublicPage
     */
    public function publickey()
    {
        return $this->handleNotFound(function () {
            $data = [
                "publickey" => $this->public_key,
                "privatekey" => $this->private_key
            ];
            return $data;
        });
    }
}
