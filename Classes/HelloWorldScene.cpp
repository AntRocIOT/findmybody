/****************************************************************************
 Copyright (c) 2017-2018 Xiamen Yaji Software Co., Ltd.

 http://www.cocos2d-x.org

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 ****************************************************************************/

#include "HelloWorldScene.h"
#include <string>
#include <iostream>
#include <experimental/filesystem>

using namespace std;
namespace fs = std::experimental::filesystem;

USING_NS_CC;
Scene* HelloWorld::createScene()
{
    return HelloWorld::create();
}

// Print useful error message instead of segfaulting when files are not there.
static void problemLoading(const char* filename)
{
    printf("Error while loading: %s\n", filename);
    printf("Depending on how you compiled you might have to add 'Resources/' in front of filenames in HelloWorldScene.cpp\n");
}

// on "init" you need to initialize your instance
bool HelloWorld::init()
{
    if ( !Scene::init() ) {
        return false;

}

    _searchPaths.push_back("res/character/idle");

    FileUtils *fileUtils = FileUtils::getInstance();
    fileUtils->setSearchPaths(_searchPaths);

    auto origin = Director::getInstance()->getVisibleOrigin();
    auto winSize = Director::getInstance()->getVisibleSize();
    auto background = DrawNode::create();
    background->drawSolidRect(origin, winSize, Color4F(0.6,0.6,0.6,1.0));
    this->addChild(background);
// 2

// 3
    // _anim = Animation::animation();
// There are other several ways of storing + adding frames,
// this is the most basic using one image per frame.
    loadCharacter(winSize);
    //_idlePlayer->setScale(0.1);
    //_player->setPosition(Vec2(winSize.width * 0.2, winSize.height * 0.5));
    //this->addChild(_player);
    //auto animation = Animation::createWithSpriteFrames(frames, 1.0f/8);
    //sprite->runAction(RepeatForever::create(Animate::create(animation)));

// 4
    //_player = Sprite::create(newspriteFrame);
    //_player->setScale(0.1);
    //_player->setPosition(Vec2(winSize.width * 0.2, winSize.height * 0.5));
    //this->addChild(_player);

    return true;
}
void HelloWorld::loadCharacter(cocos2d::Size winS){
    _spriteCache = SpriteFrameCache::getInstance();
    _spriteCache->addSpriteFramesWithFile("head-0.plist");
    for (int i = 1; i < 3; i++)
    {
     std::string num = StringUtils::format("%d", i);
     _idlePlayer.pushBack(_spriteCache->getSpriteFrameByName("head" + num + ".png"));
    }
    _idleAnimation = Animation::createWithSpriteFrames(_idlePlayer, 0.05f);
    _idleAnimation->retain();
// use/run the animation
    auto temp_sprite = Sprite::create();

    temp_sprite->setAnchorPoint(Vec2(0.5,0.5));
    temp_sprite->setPosition(Vec2(winS.width * 0.2, winS.height * 0.5));
    temp_sprite->setScale(0.1);
    this->addChild(temp_sprite);
    auto walk = Animate::create(_idleAnimation);
    temp_sprite->runAction(RepeatForever::create(walk));
}


void HelloWorld::menuCloseCallback(Ref* pSender)
{
    //Close the cocos2d-x game scene and quit the application
    Director::getInstance()->end();

    /*To navigate back to native iOS screen(if present) without quitting the application  ,do not use Director::getInstance()->end() as given above,instead trigger a custom event created in RootViewController.mm as below*/

    //EventCustom customEndEvent("game_scene_close_event");
    //_eventDispatcher->dispatchEvent(&customEndEvent);


}
