<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\Controller;
use OCP\Template;
use OCP\IRequest;

/**
- Define a new page controller
 */

class PageController extends Controller
{
    private $userId;

    /**
     * @var IURLGenerator
     */
    protected $urlGenerator;

    /**
     * @var UrlService
     */
    protected $urlService;

    protected $rdsService;

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
        $this->userId = $userId;
        $this->clientMapper = $clientMapper;
        $this->userSession = $userSession;
        $this->urlGenerator = $urlGenerator;
        $this->rdsService = $rdsService;
        $this->urlService = $rdsService->getUrlService();
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */

    public function index()
    {
        $userId = $this->userSession->getUser()->getUID();
        $t = new Template('rds', 'main.research');
        $t->assign('clients', $this->clientMapper->findByUser($userId));
        $t->assign('user_id', $userId);
        $t->assign('urlGenerator', $this->urlGenerator);
        $t->assign("cloudURL", $this->urlService->getURL());
        $t->assign("oauthname", $this->rdsService->getOauthValue());
        return $t;
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
            return $data;
        });
    }
}
