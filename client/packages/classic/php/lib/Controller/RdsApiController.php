<?php

namespace OCA\RDS\Controller;

require __DIR__ . '/../../vendor/autoload.php';

use Jose\Component\KeyManagement\JWKFactory;
use Jose\Component\Core\Util\RSAKey;

use \OCA\OAuth2\Db\ClientMapper;
use OCP\IUserSession;
use OCP\IURLGenerator;
use \OCA\RDS\Service\RDSService;

use OCP\IRequest;
use OCP\AppFramework\{
    ApiController,
};
use OCP\IConfig;

/**
- Define a new api controller
 */

class RdsApiController extends ApiController
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
     * @CORS
     * @NoAdminRequired
     * @NoCSRFRequired
     *
     * Returns the user informations
     *
     * @return object the informations as jwt
     */
    public function informations()
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
     * @PublicPage
     * @CORS
     *
     * Returns the public key for mailadress
     *
     * @return object an object with publickey
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
