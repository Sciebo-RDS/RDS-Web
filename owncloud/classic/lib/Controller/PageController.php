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
}
