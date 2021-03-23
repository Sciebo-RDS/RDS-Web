<?php

namespace OCA\RDS\Controller;

require __DIR__ . '/../../vendor/autoload.php';

use Jose\Component\Core\AlgorithmManager;
use Jose\Component\Core\JWK;
use Jose\Component\Signature\Algorithm\RS256;
use Jose\Component\Signature\JWSBuilder;
use Jose\Component\KeyManagement\JWKFactory;
use Jose\Component\Signature\Serializer\CompactSerializer;
use Jose\Component\Core\Util\RSAKey;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};
use OCP\IConfig;

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
    private $jwsBuilder;

    private $config;

    use Errors;


    public function __construct(
        $AppName,
        IRequest $request,
        $userId,
        ClientMapper $clientMapper,
        IUserSession $userSession,
        IURLGenerator $urlGenerator,
        RDSService $rdsService,
        IConfig $config
    ) {
        parent::__construct($AppName, $request);
        $this->appName = $AppName;
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();

        $this->config = $config;

        $this->jwk = RSAKey::createFromJWK(JWKFactory::createRSAKey(
            4096 // Size in bits of the key. We recommend at least 2048 bits.
        ));

        $this->private_key = $this->config->getAppValue("rds", "privatekey", "");
        $this->public_key = $this->config->getAppValue("rds", "publickey", "");

        if ($this->private_key === "") {
            $this->public_key = RSAKey::toPublic($this->jwk)->toPEM();
            $this->private_key = $this->jwk->toPEM();

            $this->config->setAppValue("rds", "privatekey", $this->private_key);
            $this->config->setAppValue("rds", "publickey", $this->public_key);
        }
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
        $policy->addAllowedFontDomain("https://fonts.gstatic.com");
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

            $token = \Firebase\JWT\JWT::encode($data, $this->private_key, 'RS256');

            return ["jwt" => $token];
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
                "publickey" =>  $this->public_key
            ];
            return $data;
        });
    }
}
