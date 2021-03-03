<?php

namespace OCA\RDS\Controller;

use OCP\AppFramework\{
    Controller,
    Http\TemplateResponse
};

use OCP\IRequest;

/**
- Define a new page controller
 */

class PageController extends Controller
{
    private $userId;

    use Errors;

    public function __construct($AppName, IRequest $request, $userId)
    {
        parent::__construct($AppName, $request);
        $this->userId = $userId;
    }

    /**
     * @NoCSRFRequired
     * @NoAdminRequired
     */

    public function index()
    {
        return new TemplateResponse('rds', 'main.research');;
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
